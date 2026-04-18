def test_register_success(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "newuser",
        "password": "pass123",
        "role": "VIEWER"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"

def test_register_duplicate(client):
    client.post("/api/v1/auth/register", json={
        "username": "dupuser",
        "password": "pass123",
        "role": "VIEWER"
    })
    response = client.post("/api/v1/auth/register", json={
        "username": "dupuser",
        "password": "pass123",
        "role": "VIEWER"
    })
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "username": "loginuser",
        "password": "pass123",
        "role": "ADMIN"
    })
    response = client.post("/api/v1/auth/login", json={
        "username": "loginuser",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "ADMIN"

def test_login_wrong_password(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_login_wrong_username(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "nobody",
        "password": "pass123"
    })
    assert response.status_code == 401