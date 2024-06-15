
import requests
import json
BASE_URL = "http://127.0.0.1:8000/api"

def login(email, password):
    url = f"{BASE_URL}/login/"
    data = {
        'username': email,
        'password': password
    }
    response = requests.post(url, json=data)
    print(response.text)
    return response.json()


def search_users(token, query):
    url = f"{BASE_URL}/search/"
    headers = {
        'Authorization': f'Token {token}'
    }
    params = {'q': query}
    response = requests.get(url, headers=headers, params=params)
    print(response.text)
    return response.json()


# Login
email = "test1@example.com"
password = "password123"
login_response = login(email, password)
print("Login Response:", login_response)
token = login_response.get('token')
query= "qm"
search_users(token, query)