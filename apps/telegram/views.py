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
async def start(message: types.Message):
    user_id = message.from_user.id  # Уникальный ID пользователя

    # Используйте только уникальный user_id для get_or_create
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        user_id=user_id,
        defaults={
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'user_role': "User"
        }
    )

    if created:
        # Если создан новый пользователь
        await message.answer(f"Привет, новый пользователь {message.from_user.full_name}!", reply_markup=profile_keyboard)
    else:
        # Если пользователь уже существует
        await message.answer(f"С возвращением, {message.from_user.full_name}!", reply_markup=profile_keyboard)

""""Фукнция для показа профиля пользователя"""
@dp.message_handler(text="Профиль")
async def get_user_profile(message:types.Message):
    user = await sync_to_async(TelegramUser.objects.get)(user_id=message.from_user.id)
    await message.answer(f"""<b>Вот ваш профиль</b>
<b>Имя:</b> {user.first_name}
<b>Фамилия:</b> {user.last_name}
<b>Имя пользователя:</b> @{user.username}
<b>ID:</b> {message.from_user.id}
<b>Статус пользователя:</b> {user.user_role}""", parse_mode="HTML")

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

@dp.message_handler(text="Заказы")
async def get_delivery_orders(message: types.Message):
    user = await sync_to_async(TelegramUser.objects.get)(
        user_id=message.from_user.id
    )

    if user.user_role == "Delivery":
        recent_deliveries = await sync_to_async(list)(
            BillingDelivery.objects.filter(telegram_user=user).order_by('-created')[:5]
        )

        if recent_deliveries:
            deliveries_info = []

            for delivery in recent_deliveries:
                delivery_info = f"<b>ID доставки:</b> {delivery.id}\n<b>Статус:</b> {delivery.get_delivery_display()}\n<b>Дата:</b> {delivery.created.strftime('%d-%m-%Y %H:%M')}"
                
                # Get delivery history for each delivery
                delivery_histories = await sync_to_async(list)(delivery.delivery_history.all().order_by('-created'))
                if delivery_histories:
                    history_info = "\n".join([f"    - {history.created.strftime('%d-%m-%Y %H:%M')}: {history.message}" for history in delivery_histories])
                    delivery_info += f"\n<b>История доставки:</b>\n" + history_info

                deliveries_info.append(delivery_info)

            final_message = "Вот ваши последние заказы которые вы делали:\n\n" + "\n\n".join(deliveries_info)
            await message.answer(final_message, parse_mode='HTML')
        else:
            await message.answer("У вас нет недавних заказов.")
    else:
        await message.answer("Вы не являетесь курьером")

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
            telegram_user_instance, created = await sync_to_async(TelegramUser.objects.get_or_create)(
                id=callback_query.message.from_user.id
            )

            delivery_create = await sync_to_async(BillingDelivery.objects.create)(
                billing_id=int(id_billing),
                telegram_user_id=user.id,
                delivery="Accepted",
                telegram_user=telegram_user_instance
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
async def send_post_billing(id, products, payment_method, payment_code, address, phone, delivery_price, total_price):
    await bot.send_message(-4013644681, f"""<b>Биллинг #{id}</b>
<b>Товары:</b> 
{products}
<b>Способ оплаты:</b> {payment_method}
<b>Код оплаты:</b> {payment_code}
<b>Адрес:</b> {address}
<b>Номер:</b> {phone}
<b>Доставка:</b> {delivery_price} KGS
<b>Итого c доставкой:</b> {total_price} KGS
<b>Статус:</b> Ожидание курьера""",
reply_markup=billing_keyboard, parse_mode='HTML')
    
"""Функция для отправки биллинга меню в телеграм группу"""
async def send_post_billing_menu(id, table_uuid, products, payment_method, payment_code, total_price):
    await bot.send_message(-1002071470870, f"""<b>Заказ на столик {table_uuid} #{id}</b>
<b>Товары:</b> {products}
<b>Способ оплаты:</b> {payment_method}
<b>Код оплаты:</b> {payment_code}
<b>Итого:</b> {total_price} KGS
<b>Статус:</b> Ожидание официанта""",
reply_markup=billing_menu_keyboard, parse_mode='HTML')
    
@dp.callback_query_handler(lambda call: call.data == "confirm_menu_order")
async def menu_order_conifirm_waiter(callback_query: types.CallbackQuery):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=int(callback_query["from"]["id"]))
        id_billing = callback_query.message.text.split()[1].replace('#', '')
        print(id_billing)
        print(user.id)
        if user.user_role == "Waiter":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"{callback_query.message.text }\nСтатус: Принят официантом @{user.username}",
                # reply_markup=billing_keyboard  # Если вы хотите также обновить клавиатуру
            )
            await bot.answer_callback_query(callback_query.id, text=f"Вы успешно взяли заказ {id_billing}")
            await bot.send_message(user.user_id, f"{callback_query.message.text}", reply_markup=order_keyboard)
        else:
            await bot.answer_callback_query(callback_query.id, text="Вы не можете взять заказ")
    except Exception as error:
        print(error)
        await bot.answer_callback_query(callback_query.id, text="Зарегистрируйтесь в боте /start")