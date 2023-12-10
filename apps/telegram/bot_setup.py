from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from django.conf import settings

API_TOKEN = settings.TELEGRAM_BOT_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
basicConfig(level=INFO)