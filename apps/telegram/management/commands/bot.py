from typing import Any, Optional
from django.core.management.base import BaseCommand

from apps.telegram.bot_setup import dp, executor
import apps.telegram.support  # Импорт модуля поддержки


class Command(BaseCommand):
    help = "Start Bot Aiogram"

    def handle(self, *args: Any, **options: Any) -> str | None:
        print("START BOT")
        executor.start_polling(dp, skip_updates=True)