from dotenv import load_dotenv
import requests
import json
import os

def main():
    load_dotenv('/home/binniev/Desktop/django_projects/DoyobisanDelivery/.env')

    host = "https://api-ru.iiko.services"

    token = get_access_token_iiko(f"{host}/api/1/access_token")

    if token:
        organization_id = get_organization_id(f'{host}/api/1/organizations', token)
        print(f"ID: {organization_id}")
        external_menu_id = get_menu(f"{host}/api/2/menu", token)
        print(external_menu_id)
        get_detail_menu(f'{host}/api/1/nomenclature', token, organization_id)
        menu_by_id_url = f"{host}/api/2/menu/by_id"
        result_menu = get_menu_by_id(menu_by_id_url, token, external_menu_id, organization_id)
        # print(result_menu)
        return result_menu

def get_access_token_iiko(url):
    payload = {
        "apiLogin": os.environ.get("IIKO_TOKEN")
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        token = response_data['token']
        return token
    else:
        print(f'Ошибка при получении токена {response.text}. Код статуса: {response.status_code}')
        return None

def get_organization_id(url, token):
    # Замените это на ваши данные
    payload = {
        "organizationIds": [
            "497f6eca-6276-4993-bfeb-53cbbbba6f08"
        ],
        "returnAdditionalInfo": True,
        "includeDisabled": True,
        "returnExternalData": [
            "string"
        ]
    }

    # Устанавливаем заголовок для указания типа контента
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Отправляем POST-запрос с данными параметрами
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Проверяем, был ли запрос успешным
    if response.status_code == 200:
        # Распаковываем ответ в формате JSON
        response_data = response.json()
        # Обработка ответа
        return response_data['organizations'][0]['id']
    else:
        print(f'Ошибка при выполнении запроса. Код статуса: {response.status_code}')

def get_menu(url, token):
    access_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    payload = {
        "organizationId": "7bc05553-4b68-44e8-b7bc-37be63c6d9e9",
        "startRevision": 0
    }

    response = requests.post(url, data=json.dumps(payload), headers=access_headers)

    if response.status_code == 200:
        response_data = response.json()
        # Обработка ответа
        return response_data['externalMenus'][0]['id']
    else:
        print(f'Ошибка при выполнении запроса {response.text}. Код статуса: {response.status_code}')

def get_detail_menu(url, token, organization_id):
    # Замените это на ваши данные
    payload = {
        "organizationId": organization_id,
        "startRevision": 0
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Отправляем POST-запрос с данными параметрами
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Проверяем, был ли запрос успешным
    if response.status_code == 200:
        # Распаковываем ответ в формате JSON
        response_data = response.json()
        return response_data['productCategories'][0]['id']
    else:
        print(f'Ошибка при выполнении запроса {response.text}. Код статуса: {response.status_code}')
            
def get_menu_by_id(url, token, external_menu_id, organization_ids):
    access_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    organization_ids_list = []
    organization_ids_list.append(organization_ids)
    payload = {
        "externalMenuId": external_menu_id,
        "organizationIds": [
            organization_ids
        ],
    }

    response = requests.post(url, data=json.dumps(payload), headers=access_headers)

    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        print(f'Ошибка при выполнении запроса {response.text}. Код статуса: {response.status_code}')

if __name__ == "__main__":
    main()