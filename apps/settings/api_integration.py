from django.utils.text import slugify
import logging

from apps.products.models import Product
from apps.categories.models import Category
from utils.iiko_menu import main

# Настройка логгера
logger = logging.getLogger(__name__)

def update_menu_from_api():
    logger.info("Выполняется запрос к API")
    api_data = main()  # Получение данных от API

    for category_data in api_data['itemCategories']:
        # Обновление или создание категории
        category, created = Category.objects.update_or_create(
            external_id=category_data['id'],
            defaults={
                'title': category_data['name'],
                'slug': slugify(category_data['name'])
            }
        )

        for item in category_data['items']:
            for size in item['itemSizes']:
                sku = size['sku']
                title = item['name']
                description = item.get('description', '')
                price = size['prices'][0]['price']
                image_url = size.get('buttonImageUrl', '')

                # Поиск существующего продукта или создание нового
                product, created = Product.objects.update_or_create(
                    sku=sku,
                    defaults={
                        'title': title,
                        'description': description,
                        'price': str(price),
                        'category': category,
                        'image': image_url  # Загрузка изображений может потребовать дополнительной обработки
                    }
                )

                if created:
                    logger.info(f"Добавлен новый продукт: {product.title}")
                else:
                    logger.info(f"Обновлен продукт: {product.title}")

    logger.info("Обновление базы данных завершено")