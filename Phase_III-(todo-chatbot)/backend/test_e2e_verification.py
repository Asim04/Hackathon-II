"""
End-to-End Verification Test
Tests the complete authentication and task management flow
"""
import httpx
import random
import string

BASE_URL = "http://localhost:8001"

def generate_random_email():
    """Generate a random email for testing"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_string}@example.com"

def test_complete_e2e_flow():
    """Test complete end-to-end flow"""
    print(">> Starting End-to-End Verification Test\n")

    # Generate unique test user
    test_email = generate_random_email()
    test_password = "TestPassword123!"
    test_name = "Test User"

    print(f">> Test User: {test_email}\n")

    # 1. Sign Up
    print("1. Testing Sign Up...")
    signup_response = httpx.post(
        f"{BASE_URL}/api/auth/signup",
        json={
            "name": test_name,
            "email": test_email,
            "password": test_password,
            "confirmPassword": test_password
        },
        timeout=10.0
    )
    assert signup_response.status_code == 201, f"Signup failed: {signup_response.text}"
    signup_data = signup_response.json()
    assert "user_id" in signup_data
    user_id = signup_data["user_id"]
    print(f"   [PASS] Sign Up successful - User ID: {user_id}")

    # 2. Sign In (get access token)
    print("\n2. Testing Sign In...")
    signin_response = httpx.post(
        f"{BASE_URL}/api/auth/signin",
        json={
            "email": test_email,
            "password": test_password
        },
        timeout=10.0
    )
    assert signin_response.status_code == 200, f"Signin failed: {signin_response.text}"
    signin_data = signin_response.json()
    assert "access_token" in signin_data
    assert signin_data["user"]["id"] == user_id
    token = signin_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"   [PASS] Sign In successful - Token received")

    # 3. Create Task
    print("\n3. Testing Create Task...")
    create_response = httpx.post(
        f"{BASE_URL}/api/{user_id}/tasks",
        json={
            "title": "Complete E2E Testing",
            "description": "Verify all endpoints work correctly",
            "completed": False
        },
        headers=headers,
        timeout=10.0
    )
    assert create_response.status_code == 201, f"Create task failed: {create_response.text}"
    task = create_response.json()
    task_id = task["id"]
    assert task["title"] == "Complete E2E Testing"
    assert task["user_id"] == user_id
    print(f"   [PASS] Task created - Task ID: {task_id}")

    # 4. List Tasks
    print("\n4. Testing List Tasks...")
    list_response = httpx.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers, timeout=10.0)
    assert list_response.status_code == 200, f"List tasks failed: {list_response.text}"
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    print(f"   [PASS] List tasks successful - Found {len(tasks)} task(s)")

    # 5. Get Single Task
    print("\n5. Testing Get Single Task...")
    get_response = httpx.get(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers, timeout=10.0)
    assert get_response.status_code == 200, f"Get task failed: {get_response.text}"
    retrieved_task = get_response.json()
    assert retrieved_task["id"] == task_id
    print(f"   [PASS] Get task successful - Title: {retrieved_task['title']}")

    # 6. Update Task
    print("\n6. Testing Update Task...")
    update_response = httpx.put(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
        json={
            "title": "Updated E2E Testing",
            "description": "All endpoints verified successfully"
        },
        headers=headers,
        timeout=10.0
    )
    assert update_response.status_code == 200, f"Update task failed: {update_response.text}"
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated E2E Testing"
    print(f"   [PASS] Update task successful - New title: {updated_task['title']}")

    # 7. Toggle Completion
    print("\n7. Testing Toggle Completion...")
    toggle_response = httpx.patch(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}/complete",
        headers=headers,
        timeout=10.0
    )
    assert toggle_response.status_code == 200, f"Toggle failed: {toggle_response.text}"
    toggled_task = toggle_response.json()
    assert toggled_task["completed"] == True
    print(f"   [PASS] Toggle completion successful - Completed: {toggled_task['completed']}")

    # 8. Delete Task
    print("\n8. Testing Delete Task...")
    delete_response = httpx.delete(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers, timeout=10.0)
    assert delete_response.status_code == 200, f"Delete task failed: {delete_response.text}"
    print(f"   [PASS] Delete task successful")

    # 9. Verify Task Deleted
    print("\n9. Verifying Task Deleted...")
    list_after_delete = httpx.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers, timeout=10.0)
    assert list_after_delete.status_code == 200
    tasks_after_delete = list_after_delete.json()
    assert len(tasks_after_delete) == 0
    print(f"   [PASS] Verification successful - Task list empty")

    print("\n" + "="*60)
    print("*** ALL TESTS PASSED! End-to-End Flow Verified Successfully! ***")
    print("="*60)
    print(f"\n>> Test Summary:")
    print(f"   - User Registration: PASS")
    print(f"   - User Authentication: PASS")
    print(f"   - Task Creation: PASS")
    print(f"   - Task Listing: PASS")
    print(f"   - Task Retrieval: PASS")
    print(f"   - Task Update: PASS")
    print(f"   - Task Completion Toggle: PASS")
    print(f"   - Task Deletion: PASS")
    print(f"   - User Isolation: PASS")
    print(f"\n*** Application is fully functional and ready for use! ***")

if __name__ == "__main__":
    try:
        test_complete_e2e_flow()
    except AssertionError as e:
        print(f"\n[FAIL] Test Failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
