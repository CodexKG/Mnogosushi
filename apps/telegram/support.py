from apps.telegram.bot_setup import dp, types

print("Support module is being imported and executed")

@dp.message_handler(text='Поддержка')
async def contact_support(message: types.Message):
    await message.answer(f"Здравствуйте {message.from_user.full_name}! Чем могу помочь?")