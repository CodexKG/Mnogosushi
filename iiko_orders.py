from dotenv import load_dotenv
import requests
import json
import os

load_dotenv('.env')

host = "https://api-ru.iiko.services"

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

token = get_access_token_iiko(f"{host}/api/1/access_token")
print(token)

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

call_organization_id = get_organization_id(f'{host}/api/1/organizations', token)
print(call_organization_id)

def terminal_groups(url, token, organization_id):
    # Замените это на ваши данные
    payload = {
        "organizationIds": [
            f"{organization_id}"
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
    print(response.json())

terminal_groups(f'{host}/api/1/terminal_groups', token, call_organization_id)