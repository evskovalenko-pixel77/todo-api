def test_create_task(client, user_token_headers):
    response = client.post("/tasks", json={"title": "My Task"}, headers=user_token_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data

def test_list_tasks_empty(client, user_token_headers):
    response = client.get("/tasks", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_list_tasks_with_items(client, user_token_headers):
    client.post("/tasks", json={"title": "Task 1"}, headers=user_token_headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=user_token_headers)
    response = client.get("/tasks", headers=user_token_headers)
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2

def test_get_task_by_id(client, user_token_headers):
    create_resp = client.post("/tasks", json={"title": "Specific"}, headers=user_token_headers)
    task_id = create_resp.json()["id"]
    response = client.get(f"/tasks/{task_id}", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Specific"

def test_get_task_not_found(client, user_token_headers):
    response = client.get("/tasks/9999", headers=user_token_headers)
    assert response.status_code == 404

def test_get_task_of_other_user(client, db_session):
    # create user2 and task, then try to access with user1's token
    from app.auth.models import User
    from app.auth.services import register_user
    from app.tasks.services import create_task
    email1 = "user1@example.com"
    email2 = "user2@example.com"
    password = "pass123"
    register_user(db_session, email1, password)
    user2 = register_user(db_session, email2, password)
    task = create_task(db_session, user2.id, "User2 Task")
    from app.core.security import create_access_token
    token = create_access_token(subject=1)  # user1 id=1
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/tasks/{task.id}", headers=headers)
    assert response.status_code == 404

def test_update_task(client, user_token_headers):
    create_resp = client.post("/tasks", json={"title": "Update Me"}, headers=user_token_headers)
    task_id = create_resp.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": "Updated", "completed": True}, headers=user_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True

def test_update_task_not_found(client, user_token_headers):
    response = client.patch("/tasks/9999", json={"title": "won't work"}, headers=user_token_headers)
    assert response.status_code == 404

def test_delete_task(client, user_token_headers):
    create_resp = client.post("/tasks", json={"title": "Delete Me"}, headers=user_token_headers)
    task_id = create_resp.json()["id"]
    response = client.delete(f"/tasks/{task_id}", headers=user_token_headers)
    assert response.status_code == 204
    # verify it's gone
    get_resp = client.get(f"/tasks/{task_id}", headers=user_token_headers)
    assert get_resp.status_code == 404

def test_delete_task_not_found(client, user_token_headers):
    response = client.delete("/tasks/9999", headers=user_token_headers)
    assert response.status_code == 404

def test_unauthorized_access(client):
    response = client.get("/tasks")
    assert response.status_code == 401
