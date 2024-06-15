import requests

BASE_URL = "http://127.0.0.1:8000/api"

def signup(email, password):
    url = f"{BASE_URL}/signup/"
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, json=data)
    return response.json()

def login(email, password):
    url = f"{BASE_URL}/login/"
    data = {
        'username': email,
        'password': password
    }
    response = requests.post(url, json=data)
    return response.json()


def search_users(token, query):
    url = f"{BASE_URL}/search/"
    headers = {
        'Authorization': f'Token {token}'
    }
    params = {'q': query}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def send_friend_request(token, to_user_id):
    url = f"{BASE_URL}/friend-requests/"
    headers = {
        'Authorization': f'Token {token}'
    }
    data = {
        'to_user': to_user_id
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    return response.json()

def accept_friend_request(token, request_id):
    url = f"{BASE_URL}/friend-requests/{request_id}/accept/"
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.post(url, headers=headers)
    # print(response.text)
    return response.json()

def reject_friend_request(token, request_id):
    url = f"{BASE_URL}/friend-requests/{request_id}/reject/"
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.post(url, headers=headers)
    return response.json()

def list_friends(token):
    url = f"{BASE_URL}/friends/"
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def list_pending_friend_requests(token):
    url = f"{BASE_URL}/friend-requests/pending/"
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()
# Example usage
if __name__ == "__main__":
    email = "sam@gmail.com"
    password = "password123"
    
    # Signup
    # signup_response = signup(email, password)
    # print("Signup Response:", signup_response)

    # Login
    login_response = login(email, password)
    print("Login Response:", login_response)
    token = login_response.get('token')

    if token:
        # Search Users
        search_response = search_users(token, "am")
        print("Search Users Response:", search_response)

        # Send Friend Request
        to_user_id = 1  # Replace with the actual user ID you want to send a friend request to
        friend_request_response = send_friend_request(token, to_user_id)
        print("Send Friend Request Response:", friend_request_response)

        # List Friends
        friends_list_response = list_friends(token)
        print("Friends List Response:", friends_list_response)

        # List Pending Friend Requests
        pending_requests_response = list_pending_friend_requests(token)
        print("Pending Friend Requests Response:", pending_requests_response)
