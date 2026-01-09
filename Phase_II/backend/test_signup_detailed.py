import httpx
import json
import traceback

# Test signup endpoint with detailed error handling
print("Testing signup endpoint with detailed error handling...")
signup_data = {
    "name": "Test User",
    "email": "testuser2@example.com",
    "password": "SecurePass123!"
}

try:
    response = httpx.post(
        "http://localhost:8001/api/auth/signup",
        json=signup_data,
        timeout=10.0
    )
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response: {response.text}")

    if response.status_code == 201:
        print(f"\n✅ SUCCESS! User created:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"\n❌ FAILED with status {response.status_code}")

except Exception as e:
    print(f"❌ Exception occurred: {e}")
    traceback.print_exc()

# Test health endpoint to confirm server is running
print("\n" + "="*50)
print("Testing health endpoint...")
try:
    response = httpx.get("http://localhost:8001/health", timeout=5.0)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Health check failed: {e}")
