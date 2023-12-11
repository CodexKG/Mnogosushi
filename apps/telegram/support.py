from asgiref.sync import sync_to_async
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from apps.telegram.bot_setup import dp, bot, types
from apps.telegram.keyboards import support_keyboard, support_action_keyboard
from apps.telegram.models import TechnicalSupport, TelegramUser

print("Support module is being imported and executed")

@dp.message_handler(text='Поддержка')
async def contact_support(message: types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}! Чем могу помочь?", reply_markup=support_keyboard)

class SupportState(StatesGroup):
    message = State()

@dp.message_handler(text='Обратиться к технической поддержке')
async def call_support(message: types.Message):
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
<b>ID:</b> {created_support.created}
""", parse_mode="HTML", reply_markup=support_action_keyboard)
        await message.answer(f"Уважаемый {message.from_user.full_name}, вы обратились в техническую поддержку.\nОжидайте ответ от специалистов\nID обращения: {created_support.id}")
    
    await state.finish()