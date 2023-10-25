from utils.iiko_menu import main
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
import sqlite3
import os

load_dotenv('.env')

def parser_postgresql():
    try:
        # Настройка соединение с базой данных
        connection = psycopg2.connect(
            database = os.environ.get("DB_NAME"),
            user = os.environ.get("DB_USER"),
            password = os.environ.get("DB_USER_PASSWORD"),
            host = os.environ.get("DB_HOST"),
            port = os.environ.get("DB_PORT")
        )
        connection.autocommit = True
        print(connection)
        print("База данных готова к работе...")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products_product;")
        result = cursor.fetchall()
        print(result)

        menu_data = main()
        # Получаем информацию о продуктах
        items = menu_data.get('itemCategories', [])[0].get('items')

        products = []
        for item in items:
            price = item['itemSizes'][0].get('prices')[0].get('price')
            description = item.get('description', None)  # Устанавливаем значение None, если описание отсутствует
            if price:
                item_info = {
                    'title': item['name'],
                    'price': price,
                    'description': description,
                }
                products.append(item_info)

        for product in products:
            cursor.execute(f"""INSERT INTO products_product (title, description, price, image, created) 
                        VALUES ('{product['title'].title()}', '{product['description']}', 
                        {product['price']}, 'no_image.jpg', '{datetime.now()}');""")
            print(product)
        print("Данные успешно переданы")
    except Exception as error:
        print(error)
    finally:
        connection.close()

def parser_sqlite():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products_product;")
    result = cursor.fetchall()
    print(result)

    menu_data = main()
    # Получаем информацию о продуктах
    items = menu_data.get('itemCategories', [])[0].get('items')

    products = []
    for item in items:
        price = item['itemSizes'][0].get('prices')[0].get('price')
        description = item.get('description', None)  # Устанавливаем значение None, если описание отсутствует
        if price:
            item_info = {
                'title': item['name'],
                'price': price,
                'description': description,
            }
            products.append(item_info)

    for product in products:
        cursor.execute(f"""INSERT INTO products_product (title, description, price, image, created) 
                        VALUES ('{product['title'].title()}', '{product['description']}', 
                        {product['price']}, 'no_image.jpg', '{datetime.now()}');""")
        print(product)
        cursor.connection.commit()
        print("Данные успешно переданы")

if __name__ == "__main__":
    parser_sqlite()