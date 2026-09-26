def test_register_and_login(client):
    registration = client.post(
        "/api/v1/auth/register",
        json={"email": "person@example.com", "password": "secure-pass-123", "full_name": "Person"},
    )
    assert registration.status_code == 201
    assert registration.json()["email"] == "person@example.com"
    assert "hashed_password" not in registration.json()

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "person@example.com", "password": "secure-pass-123"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"


def test_protected_route_rejects_missing_token(client):
    assert client.get("/api/v1/users/me").status_code == 401