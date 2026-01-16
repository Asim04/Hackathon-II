"""
Comprehensive test script for task CRUD endpoints with proper authentication.
"""
import httpx
import json

BASE_URL = "http://localhost:8001"

def test_complete_task_flow():
    """Test complete task CRUD flow with authentication."""
    print("=" * 60)
    print("COMPLETE TASK CRUD FLOW TEST")
    print("=" * 60)

    # Step 1: Sign in to get JWT token and user_id
    print("\n[1] Signing in to get JWT token and user_id...")
    signin_response = httpx.post(
        f"{BASE_URL}/api/auth/signin",
        json={
            "email": "httptest@example.com",
            "password": "SecurePass123!"
        },
        timeout=10.0
    )

    if signin_response.status_code != 200:
        print(f"[FAIL] Signin failed: {signin_response.status_code}")
        print(f"Response: {signin_response.text}")
        return

    signin_data = signin_response.json()
    token = signin_data["access_token"]
    user_id = signin_data["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    print(f"[OK] Signin successful")
    print(f"  User ID: {user_id}")
    print(f"  Token: {token[:50]}...")

    # Step 2: Create a task
    print("\n[2] Creating a new task...")
    create_response = httpx.post(
        f"{BASE_URL}/api/{user_id}/tasks",
        json={
            "title": "Test Task 1",
            "description": "This is a test task created via API"
        },
        headers=headers,
        timeout=10.0
    )

    print(f"  Status: {create_response.status_code}")
    print(f"  Response: {create_response.text}")

    if create_response.status_code != 201:
        print(f"[FAIL] Task creation failed")
        return

    task = create_response.json()
    task_id = task["id"]
    print(f"[OK] Task created successfully")
    print(f"  Task ID: {task_id}")
    print(f"  Title: {task['title']}")

    # Step 3: List all tasks
    print("\n[3] Listing all tasks...")
    list_response = httpx.get(
        f"{BASE_URL}/api/{user_id}/tasks",
        headers=headers,
        timeout=10.0
    )

    print(f"  Status: {list_response.status_code}")
    if list_response.status_code == 200:
        tasks = list_response.json()
        print(f"[OK] Tasks retrieved: {len(tasks)} task(s)")
    else:
        print(f"[FAIL] Task listing failed: {list_response.text}")

    # Step 4: Get single task
    print("\n[4] Getting single task...")
    get_response = httpx.get(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
        headers=headers,
        timeout=10.0
    )

    print(f"  Status: {get_response.status_code}")
    if get_response.status_code == 200:
        print(f"[OK] Task retrieved successfully")
    else:
        print(f"[FAIL] Get task failed: {get_response.text}")

    # Step 5: Update task
    print("\n[5] Updating task...")
    update_response = httpx.put(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
        json={
            "title": "Updated Test Task",
            "description": "This task has been updated"
        },
        headers=headers,
        timeout=10.0
    )

    print(f"  Status: {update_response.status_code}")
    if update_response.status_code == 200:
        print(f"[OK] Task updated successfully")
    else:
        print(f"[FAIL] Task update failed: {update_response.text}")

    # Step 6: Toggle task completion
    print("\n[6] Toggling task completion...")
    toggle_response = httpx.patch(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}/complete",
        headers=headers,
        timeout=10.0
    )

    print(f"  Status: {toggle_response.status_code}")
    if toggle_response.status_code == 200:
        toggled = toggle_response.json()
        print(f"[OK] Task completion toggled: {toggled.get('completed', 'N/A')}")
    else:
        print(f"[FAIL] Task toggle failed: {toggle_response.text}")

    # Step 7: Delete task
    print("\n[7] Deleting task...")
    delete_response = httpx.delete(
        f"{BASE_URL}/api/{user_id}/tasks/{task_id}",
        headers=headers,
        timeout=10.0
    )

    print(f"  Status: {delete_response.status_code}")
    if delete_response.status_code == 200:
        result = delete_response.json()
        print(f"[OK] Task deleted successfully: {result.get('message', '')}")
    else:
        print(f"[FAIL] Task deletion failed: {delete_response.text}")

    print("\n" + "=" * 60)
    print("TASK CRUD FLOW TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_complete_task_flow()
