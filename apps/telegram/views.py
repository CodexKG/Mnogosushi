from django.conf import settings
from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from asgiref.sync import sync_to_async
from datetime import datetime

from apps.telegram.models import TelegramUser, BillingDelivery, BillingDeliveryHistory
from apps.telegram.keyboards import billing_keyboard, billing_menu_keyboard, on_road_keyboard, order_keyboard, profile_keyboard

# Create your views here.
bot = Bot(settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
basicConfig(level=INFO)

"""Функция для обработки комманды /start. Если пользователя нету в базе, 
бот создаст его и даст ему поль пользователя.
По желаю можно сделать его курьером"""
@dp.message_handler(commands='start')
async def start(message:types.Message):
    user = await sync_to_async(TelegramUser.objects.get_or_create)(
        username=message.from_user.username,
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        user_role="User"
    )
    await message.answer(f"Привет {message.from_user.full_name}!", reply_markup=profile_keyboard)

""""Фукнция для показа профиля пользователя"""
@dp.message_handler(text="Профиль")
async def get_user_profile(message:types.Message):
    user = await sync_to_async(TelegramUser.objects.get)(user_id=message.from_user.id)
    await message.answer(f"""ВОТ ВАШ ПРОФИЛЬ
Имя: {user.first_name}
Фамилия: {user.last_name}
Имя пользователя: @{user.username}
ID: {message.from_user.id}
Статус пользователя: {user.user_role}""")

"""Функция для удаления заказа менеджерами"""
@dp.callback_query_handler(lambda call: call.data == 'delete_order')
async def delete_order_button(callback_query: types.CallbackQuery):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=int(callback_query["from"]["id"]))
        if user.user_role == "Manager":
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
            await bot.answer_callback_query(callback_query.id, text="Успешно удалено")
        else:
            await bot.answer_callback_query(callback_query.id, text="У вас нет прав на удаления")
    except:
        await bot.answer_callback_query(callback_query.id, text="Зарегистрируйтесь в боте /start")

"""Функция для такси (в разработке)"""
@dp.callback_query_handler(lambda call: call.data == 'taxi_order')
async def taxi_order_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text="Такси")

"""Функция для получения заказа курьером, после нажатия кнопки (Взять заказ)
в базе создается запись и также в личные сообщения приходит сам заказ
где курьер может завершить заказ после получения"""
@dp.callback_query_handler(lambda call: call.data == 'take_order')
async def take_order_button(callback_query: types.CallbackQuery):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=int(callback_query["from"]["id"]))
        id_billing = callback_query.message.text.split()[1].replace('#', '')
        print(id_billing)
        print(user.id)
        if user.user_role == "Delivery":
            delivery_create = await sync_to_async(BillingDelivery.objects.create)(
                billing_id = int(id_billing),
                telegram_user_id = user.id,
                delivery = "Accepted"
            )
            delivery_history_create = await sync_to_async(BillingDeliveryHistory.objects.create)(
                delivery = delivery_create,
                message=f'Заказ принят курьером @{user.username} {datetime.now()}',
                created=datetime.now()
            )
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"{callback_query.message.text }\nСтатус: Принят курьером @{user.username}",
                # reply_markup=billing_keyboard  # Если вы хотите также обновить клавиатуру
            )
            await bot.answer_callback_query(callback_query.id, text=f"Вы успешно взяли заказ {id_billing}")
            await bot.send_message(user.user_id, f"{callback_query.message.text}", reply_markup=order_keyboard)
        else:
            await bot.answer_callback_query(callback_query.id, text="Вы не можете взять заказ")
    except Exception as error:
        print(error)
        await bot.answer_callback_query(callback_query.id, text="Зарегистрируйтесь в боте /start")

from asgiref.sync import sync_to_async

"""Функция delivery_on_road (В пути) используется курьером после получения заказа
чтобы в базе отображалось что курбер в пути к заказчику"""
@dp.callback_query_handler(lambda call: call.data == 'on_road')
async def delivery_on_road(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    id_billing = callback_query.message.text.split()[1].replace('#', '')
    print(id_billing)

    # Используем sync_to_async для асинхронного доступа к моделям Django
    user = await sync_to_async(TelegramUser.objects.get)(user_id=user_id)

    if user.user_role == "Delivery":
        # Асинхронно получаем объект заказа
        order = await sync_to_async(BillingDelivery.objects.get)(billing_id=int(id_billing))
        order.delivery = "On way"
        delivery_history_create = await sync_to_async(BillingDeliveryHistory.objects.create)(
            delivery = order,
            message=f'Заказ в пути курьером @{user.username} {datetime.now()}',
            created=datetime.now()
        )
        await sync_to_async(order.save)()

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=f"{callback_query.message.text }\nСтатус: В пути курьер @{user.username}",
            reply_markup=on_road_keyboard
        )
        await bot.answer_callback_query(callback_query.id, text=f"Вы в пути {id_billing}")
    else:
        await bot.answer_callback_query(callback_query.id, text=f"У вас нет прав, свяжитесь с менеджерами")

@dp.callback_query_handler(lambda call: call.data == "cancel_order")
async def delivery_cancel_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    id_billing = callback_query.message.text.split()[1].replace('#', '')
    print("Billing ID:", id_billing)

    # Используем sync_to_async для асинхронного доступа к моделям Django
    user = await sync_to_async(TelegramUser.objects.get)(user_id=user_id)
    
    if user.user_role == "Delivery":
        # Асинхронно получаем объект заказа
        order = await sync_to_async(BillingDelivery.objects.get)(billing_id=int(id_billing))
        order.delivery = "Cancelled"  # Измените статус на "Отменен"
        delivery_history_create = await sync_to_async(BillingDeliveryHistory.objects.create)(
            delivery = order,
            message=f'Заказ отменен курьером @{user.username} {datetime.now()}',
            created=datetime.now()
        )
        await sync_to_async(order.save)()

        # Редактируем существующее сообщение
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
        new_message_text = f"""{callback_query.message.text }\nСтатус: Отменен курьером @{user.username}"""
        await bot.edit_message_text(new_message_text, chat_id, message_id)
        await bot.send_message(-4013644681, f"Биллинг #{id_billing}\nСтатус: Отменен курьером @{user.username}")
        await bot.send_message(-4013644681, f"{callback_query.message.text }\nСтатус: Отменен курьером @{user.username}", reply_markup=billing_keyboard)
        await sync_to_async(order.delete)()
        await bot.answer_callback_query(callback_query.id, text=f"Вы отменили заказ")
    else:
        await bot.answer_callback_query(callback_query.id, text=f"У вас нет прав, свяжитесь с менеджерами")

"""Функция (Завершить) для курьера после того как он успешно выполнил заказ"""
@dp.callback_query_handler(lambda call: call.data == "finish_order")
async def delivery_finish_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    id_billing = callback_query.message.text.split()[1].replace('#', '')

    # Используем sync_to_async для асинхронного доступа к моделям Django
    user = await sync_to_async(TelegramUser.objects.get)(user_id=user_id)
    
    if user.user_role == "Delivery":
        # Асинхронно получаем объект заказа
        order = await sync_to_async(BillingDelivery.objects.get)(billing_id=int(id_billing))
        order.delivery = "Delivered"
        delivery_history_create = await sync_to_async(BillingDeliveryHistory.objects.create)(
            delivery = order,
            message=f'Заказ выполнен курьером @{user.username} {datetime.now()}',
            created=datetime.now()
        )
        await sync_to_async(order.save)()

        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=f"{callback_query.message.text }\nСтатус: Завершен",
        )
        await bot.answer_callback_query(callback_query.id, text=f"Вы успешно завершили заказ")
    else:
        await bot.answer_callback_query(callback_query.id, text=f"У вас нет прав, свяжитесь с менеджерами")

"""Функция для отправки биллинга в телеграм группу"""
async def send_post_billing(id, products, payment_method, payment_code, address, phone, total_price):
    await bot.send_message(-4013644681, f"""Биллинг #{id}
Товары: {products}
Способ оплаты: {payment_method}
Код оплаты: {payment_code}
Адрес: {address}
Номер: {phone}
Итого: {total_price} KGS
Статус: Ожидание курьера""",
reply_markup=billing_keyboard)
    
"""Функция для отправки биллинга меню в телеграм группу"""
async def send_post_billing_menu(id, table_uuid, products, payment_method, payment_code, total_price):
    await bot.send_message(-4063835118, f"""Заказ на столик {table_uuid} #{id}
Товары: {products}
Способ оплаты: {payment_method}
Код оплаты: {payment_code}
Итого: {total_price} KGS
Статус: Ожидание официанта""",
reply_markup=billing_menu_keyboard)