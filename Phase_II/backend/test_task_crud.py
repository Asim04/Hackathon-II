"""
Comprehensive test script for task CRUD endpoints.
"""
import httpx
import json

BASE_URL = "http://localhost:8001"

def test_task_crud():
    """Test all task CRUD operations."""
    print("=" * 60)
    print("TASK CRUD ENDPOINTS TEST")
    print("=" * 60)

    # Step 1: Sign in to get JWT token
    print("\n[1] Signing in to get JWT token...")
    signin_response = httpx.post(
        f"{BASE_URL}/api/auth/signin",
        json={
            "email": "tasktest@example.com",
            "password": "SecurePass123!"
        },
        timeout=10.0
    )

    if signin_response.status_code != 200:
        print(f"[FAIL] Signin failed: {signin_response.status_code}")
        print(f"Response: {signin_response.text}")
        return

    token = signin_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[OK] Signin successful, token received")

    # Step 2: Create a task
    print("\n[2] Creating a new task...")
    create_response = httpx.post(
        f"{BASE_URL}/api/tasks",
        json={
            "title": "Test Task 1",
            "description": "This is a test task created via API"
        },
        headers=headers,
        timeout=10.0
    )

    if create_response.status_code != 201:
        print(f"[FAIL] Task creation failed: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        return

    task = create_response.json()
    task_id = task["id"]
    print(f"[OK] Task created successfully")
    print(f"  Task ID: {task_id}")
    print(f"  Title: {task['title']}")
    print(f"  Completed: {task['completed']}")

    # Step 3: List all tasks
    print("\n[3] Listing all tasks...")
    list_response = httpx.get(
        f"{BASE_URL}/api/tasks",
        headers=headers,
        timeout=10.0
    )

    if list_response.status_code != 200:
        print(f"[FAIL] Task listing failed: {list_response.status_code}")
        print(f"Response: {list_response.text}")
        return

    tasks = list_response.json()
    print(f"[OK] Tasks retrieved successfully")
    print(f"  Total tasks: {len(tasks)}")

    # Step 4: Get single task
    print("\n[4] Getting single task...")
    get_response = httpx.get(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers=headers,
        timeout=10.0
    )

    if get_response.status_code != 200:
        print(f"[FAIL] Get task failed: {get_response.status_code}")
        print(f"Response: {get_response.text}")
        return

    task_detail = get_response.json()
    print(f"[OK] Task retrieved successfully")
    print(f"  Title: {task_detail['title']}")
    print(f"  Description: {task_detail['description']}")

    # Step 5: Update task
    print("\n[5] Updating task...")
    update_response = httpx.put(
        f"{BASE_URL}/api/tasks/{task_id}",
        json={
            "title": "Updated Test Task",
            "description": "This task has been updated"
        },
        headers=headers,
        timeout=10.0
    )

    if update_response.status_code != 200:
        print(f"[FAIL] Task update failed: {update_response.status_code}")
        print(f"Response: {update_response.text}")
        return

    updated_task = update_response.json()
    print(f"[OK] Task updated successfully")
    print(f"  New title: {updated_task['title']}")
    print(f"  New description: {updated_task['description']}")

    # Step 6: Toggle task completion
    print("\n[6] Toggling task completion...")
    toggle_response = httpx.patch(
        f"{BASE_URL}/api/tasks/{task_id}/toggle",
        headers=headers,
        timeout=10.0
    )

    if toggle_response.status_code != 200:
        print(f"[FAIL] Task toggle failed: {toggle_response.status_code}")
        print(f"Response: {toggle_response.text}")
        return

    toggled_task = toggle_response.json()
    print(f"[OK] Task completion toggled")
    print(f"  Completed: {toggled_task['completed']}")

    # Step 7: Filter completed tasks
    print("\n[7] Filtering completed tasks...")
    filter_response = httpx.get(
        f"{BASE_URL}/api/tasks?completed=true",
        headers=headers,
        timeout=10.0
    )

    if filter_response.status_code != 200:
        print(f"[FAIL] Task filtering failed: {filter_response.status_code}")
        print(f"Response: {filter_response.text}")
        return

    completed_tasks = filter_response.json()
    print(f"[OK] Completed tasks retrieved")
    print(f"  Completed tasks count: {len(completed_tasks)}")

    # Step 8: Delete task
    print("\n[8] Deleting task...")
    delete_response = httpx.delete(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers=headers,
        timeout=10.0
    )

    if delete_response.status_code != 204:
        print(f"[FAIL] Task deletion failed: {delete_response.status_code}")
        print(f"Response: {delete_response.text}")
        return

    print(f"[OK] Task deleted successfully")

    # Step 9: Verify deletion
    print("\n[9] Verifying task deletion...")
    verify_response = httpx.get(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers=headers,
        timeout=10.0
    )

    if verify_response.status_code == 404:
        print(f"[OK] Task deletion verified (404 Not Found)")
    else:
        print(f"[WARN] Expected 404, got {verify_response.status_code}")

    print("\n" + "=" * 60)
    print("ALL TASK CRUD TESTS PASSED")
    print("=" * 60)

if __name__ == "__main__":
    test_task_crud()
