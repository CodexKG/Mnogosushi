from celery import shared_task
import logging

from apps.settings.api_integration import update_menu_from_api  # Предполагается, что этот метод реализован

# Настройка логгера
logger = logging.getLogger(__name__)

@shared_task
def update_menu_periodically():
    logger.info("Задача update_menu_periodically запущена")
    result = update_menu_from_api()
    logger.info(f"Результат выполнения задачи: {result}")
    return result  # Возвращение результата