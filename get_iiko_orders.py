import requests

# Replace with the actual endpoint and login provided by iiko
api_url = "https://api-ru.iiko.services/api/1/"
api_login = "14c1f5b2-5f1"

# Step 1: Authenticate and obtain token
auth_url = f"{api_url}auth/access_token"
payload = {
    "apiLogin": api_login
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(auth_url, json=payload, headers=headers)
print(response)
if response.status_code == 200:
    token = response.json()  # Or the appropriate key if the token is nested

    # Step 2: Make a request to the orders endpoint
    orders_url = f"{api_url}orders"  # Replace with the actual orders endpoint
    orders_headers = {
        "Authorization": f"Bearer {token}"
    }
    
    orders_response = requests.get(orders_url, headers=orders_headers)
    
    if orders_response.status_code == 200:
        orders = orders_response.json()  # Now you have the orders data
        print(orders)
    else:
        print("Failed to retrieve orders:", orders_response.status_code, orders_response.text)
else:
    print("Failed to authenticate:", response.status_code, response.text)
