from aiogram import types

profile_buttons = [
    types.KeyboardButton('Профиль'),
    types.KeyboardButton('Заказы'),
    types.KeyboardButton('Поддержка'),
]
profile_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*profile_buttons)

#######################################

billing_buttons = [
    types.InlineKeyboardButton('Удалить', callback_data='delete_order'),
    types.InlineKeyboardButton("Такси", callback_data='taxi_order'),
    types.InlineKeyboardButton("Взять заказ", callback_data='take_order')
]
billing_keyboard = types.InlineKeyboardMarkup().add(*billing_buttons)

order_buttons = [
    types.InlineKeyboardButton('В пути', callback_data="on_road"),
    types.InlineKeyboardButton('Отменить заказ', callback_data="cancel_order"),
]
order_keyboard = types.InlineKeyboardMarkup().add(*order_buttons)

on_road_buttons = [
    types.InlineKeyboardButton('Завершить', callback_data="finish_order")
]
on_road_keyboard = types.InlineKeyboardMarkup().add(*on_road_buttons)

#########################

billing_menu_buttons = [
    types.InlineKeyboardButton('Удалить', callback_data='not_work'),
    types.InlineKeyboardButton("Потвердить заказ", callback_data='not_working')
]
billing_menu_keyboard = types.InlineKeyboardMarkup().add(*billing_buttons)