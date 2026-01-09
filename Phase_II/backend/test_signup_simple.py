import httpx
import json

# Test signup endpoint
print("Testing signup endpoint...")
signup_data = {
    "name": "Test User",
    "email": "testuser3@example.com",
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
        print("SUCCESS! User created:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"FAILED with status {response.status_code}")

except Exception as e:
    print(f"Exception occurred: {e}")
