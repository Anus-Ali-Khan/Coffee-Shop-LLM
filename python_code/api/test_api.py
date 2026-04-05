import requests

# Test the FastAPI
url = "http://localhost:8000/chat"
data = {
    "message": "Hello, I want to order a latte",
    "session_id": "test_session"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())