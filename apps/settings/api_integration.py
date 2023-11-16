import logging

# Настройка логгера
logger = logging.getLogger(__name__)

def update_menu_from_api():
    # Логгирование начала выполнения функции
    logger.info("Выполняется запрос к API")

    # Здесь ваш код для работы с API

    # Логгирование результата
    logger.info("Данные получены, обновление базы данных")

    # Предположим, что возвращается результат
    return "WORK"