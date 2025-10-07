def test_register_user(client, db):
    """
    Test user registration successfully.
    """
    response = client.post(
        "/api/v1/register",
        json={"email": "newuser@example.com", "password": "newpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_register_existing_user(client, test_user):
    """
    Test that registering with an existing email fails.
    """
    response = client.post(
        "/api/v1/register",
        json={"email": test_user["email"], "password": "newpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_for_access_token(client, test_user):
    """
    Test successful login and token generation.
    """
    response = client.post(
        "/api/v1/token",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """
    Test login with an incorrect password.
    """
    response = client.post(
        "/api/v1/token",
        data={"username": test_user["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_wrong_email(client, test_user):
    """
    Test login with a non-existent email.
    """
    response = client.post(
        "/api/v1/token",
        data={"username": "wrong@example.com", "password": test_user["password"]},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
