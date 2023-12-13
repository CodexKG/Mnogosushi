from asgiref.sync import sync_to_async
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import ctime

from apps.telegram.bot_setup import dp, bot, types
from apps.telegram.keyboards import support_keyboard, support_action_keyboard, start_chat_keyboard, close_chat_keyboard
from apps.telegram.models import TechnicalSupport, TelegramUser

print("Support module is being imported and executed")

@dp.message_handler(text='Поддержка')
async def contact_support(message: types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}! Чем могу помочь?", reply_markup=support_keyboard)

class SupportState(StatesGroup):
    message = State()

@dp.message_handler(text='Обратиться к технической поддержке')
async def call_support(message: types.Message):
    telegram_user_id = message.from_user.id
    telegram_user, _ = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=telegram_user_id)

    # Асинхронно проверяем, есть ли уже нерешенные обращения от этого пользователя
    existing_support_request_exists = await sync_to_async(TechnicalSupport.objects.filter(
        user=telegram_user, status=False).exists)()

    if existing_support_request_exists:
        # Retrieve the first existing support request
        existing_support = await sync_to_async(TechnicalSupport.objects.filter(
            user=telegram_user, status=False).first)()

        await message.answer(f"""Уважаемый <b>{message.from_user.full_name}</b>, у вас уже есть открытое обращение в техподдержку. 
Пожалуйста, подождите ответа специалиста.
<b>ID обращения:</b> {existing_support.id}
<b>Дата обращения:</b> {existing_support.created}""", parse_mode="HTML")
    else:
        await message.reply(f"Уважаемый {message.from_user.full_name}.\nОставьте свое сообщение и в скором времени наши операторы с вами свяжутся")
        await SupportState.message.set()

@dp.message_handler(state=SupportState.message)
async def send_and_create_support(message:types.Message, state:FSMContext):
    telegram_user_id = message.from_user.id
    telegram_user, _ = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=telegram_user_id)

    # Асинхронно проверяем, есть ли уже нерешенные обращения от этого пользователя
    existing_support_request_exists = await sync_to_async(TechnicalSupport.objects.filter(
        user=telegram_user, status=False).exists)()

    if existing_support_request_exists:
        # Retrieve the first existing support request
        existing_support = await sync_to_async(TechnicalSupport.objects.filter(
            user=telegram_user, status=False).first)()

        await message.answer(f"Уважаемый {message.from_user.full_name}, у вас уже есть открытое обращение в техподдержку. Пожалуйста, подождите ответа специалиста.\nID обращения: {existing_support.id}")
    else:
        # Если нет, создаем новый объект TechnicalSupport
        created_support = await sync_to_async(TechnicalSupport.objects.create)(
            user=telegram_user,
            message=message.text,
            status=False  # По умолчанию статус False, так как запрос только создан
        )
        await bot.send_message(-4043394914, f"""Обращение в тех поддержку:
<b>Пользователь:</b> @{message.from_user.username}
<b>Дата обращения:</b> {created_support.created}
<b>Сообщение:</b> {created_support.message}
<b>ID:</b> {created_support.id}
""", parse_mode="HTML", reply_markup=support_action_keyboard)
        await message.answer(f"Уважаемый {message.from_user.full_name}, вы обратились в техническую поддержку.\nОжидайте ответ от специалистов\nID обращения: {created_support.id}")
    
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == "accept_support")
async def accept_support_manager(callback_query: types.CallbackQuery):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=int(callback_query.from_user.id))
        
        if user.user_role == "Manager":
            active_support_exists = await sync_to_async(TechnicalSupport.objects.filter(
                support_operator=user, status=False
            ).exists)()

            if not active_support_exists:
                # Используйте select_related для предварительной загрузки связанных объектов
                support_request = await sync_to_async(TechnicalSupport.objects.filter(
                    support_operator__isnull=True, status=False
                ).select_related('user').first)()

                if support_request:
                    support_request.support_operator = user
                    await sync_to_async(support_request.save)()

                    await bot.edit_message_text(
                        chat_id=callback_query.message.chat.id,
                        message_id=callback_query.message.message_id,
                        text=f"{callback_query.message.text}\nСтатус принят оператором @{user.username}"
                    )
                    await bot.send_message(user.user_id, f"{callback_query.message.text}", reply_markup=start_chat_keyboard)

                    # Теперь можно безопасно обращаться к support_request.user
                    support_user_id = support_request.user.user_id
                    await bot.send_message(support_user_id, f"Ваше обращение {support_request.id} принял оператор {user.username}")

                else:
                    await bot.answer_callback_query(callback_query.id, text="Нет доступных обращений для обработки")
            else:
                await bot.answer_callback_query(callback_query.id, text="У вас уже есть активное обращение")
        else:
            await bot.answer_callback_query(callback_query.id, text="Вы не можете взять обращение")
    except Exception as error:
        print(error)
        await callback_query.answer(f"Возникла ошибка на стороне сервера: {error}")

class MessageState(StatesGroup):
    message = State()

@dp.callback_query_handler(lambda call: call.data == "start_chat_support")
async def start_chat(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    # Обновляем сообщение, удаляя инлайн-кнопку "Начать чат"
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"{callback_query.message.text}\nЧат начат. Напишите ваше сообщение.",
        reply_markup=types.InlineKeyboardMarkup()  # Удаляем инлайн-кнопки
    )

    # Отправляем новое сообщение с обычной клавиатурой
    await bot.send_message(
        chat_id=chat_id,
        text="Вы можете начать чат.",
        reply_markup=close_chat_keyboard
    )

    # Переводим оператора в состояние ожидания сообщения
    await MessageState.message.set()

# Обработчик сообщений от оператора и пользователя
@dp.message_handler(state=MessageState.message)
async def send_message_user(message: types.Message, state: FSMContext):
    telegram_user_id = message.from_user.id

    async with state.proxy() as data:
        awaiting_reply_from = data.get('awaiting_reply_from')

        telegram_user = await sync_to_async(TelegramUser.objects.get)(user_id=telegram_user_id)
        print(telegram_user_id == awaiting_reply_from)
        print(telegram_user_id, type(telegram_user_id))
        print(awaiting_reply_from, type(awaiting_reply_from))

        if telegram_user.user_role == "Manager":
            # Получение запроса поддержки и отправка сообщения пользователю
            support_request = await sync_to_async(lambda: TechnicalSupport.objects.filter(
                support_operator=telegram_user, status=False
            ).first())()

            if support_request:
                support_user_id = await sync_to_async(lambda: support_request.user.user_id)()
                if message.text == "Закончить чат":
                    await message.answer("Вы закрыли чат")
                    support_request.status = True
                    await sync_to_async(support_request.save)()
                    await bot.send_message(support_user_id, "Чат закрыт")
                else:
                    await bot.send_message(support_user_id, message.text)
                data['awaiting_reply_from'] = int(support_user_id)
            else:
                await message.answer("Обращение не найдено.")

@dp.message_handler()
async def not_found(message:types.Message):
    telegram_user = await sync_to_async(TelegramUser.objects.get)(user_id=message.from_user.id)
    support_request = await sync_to_async(lambda: TechnicalSupport.objects.filter(
        user=telegram_user, status=False
    ).first())()
    if support_request:
        support_user_id = await sync_to_async(lambda: support_request.support_operator.user_id)()
        await bot.send_message(support_user_id, message.text)

    else:
        await message.reply(f"Я вас не понял, введите /help")