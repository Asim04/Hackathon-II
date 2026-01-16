import httpx
import json

# Test health endpoint
print("Testing health endpoint...")
response = httpx.get("http://localhost:8001/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test signup endpoint
print("Testing signup endpoint...")
signup_data = {
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "SecurePass123!"
}

try:
    response = httpx.post(
        "http://localhost:8001/api/auth/signup",
        json=signup_data,
        timeout=10.0
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 201:
        print(f"JSON: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
