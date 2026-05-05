def test_register_success(client):
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "123456"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "123456"})
    response = client.post("/auth/register", json={"email": "dup@example.com", "password": "654321"})
    assert response.status_code == 409
    assert "Email already" in response.json()["detail"]

def test_register_invalid_email(client):
    response = client.post("/auth/register", json={"email": "notanemail", "password": "123456"})
    assert response.status_code == 422

def test_register_short_password(client):
    response = client.post("/auth/register", json={"email": "user@example.com", "password": "12345"})
    assert response.status_code == 422

def test_login_success(client):
    client.post("/auth/register", json={"email": "login@example.com", "password": "secret"})
    response = client.post("/auth/login", json={"email": "login@example.com", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "login2@example.com", "password": "correct"})
    response = client.post("/auth/login", json={"email": "login2@example.com", "password": "wrong"})
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={"email": "nobody@example.com", "password": "pass"})
    assert response.status_code == 401
