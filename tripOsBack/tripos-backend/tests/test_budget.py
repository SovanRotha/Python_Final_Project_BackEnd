def test_create_budget(client, auth_headers):
    response = client.post(
        "/api/v1/budgets",
        headers=auth_headers,
        json={"name": "Japan budget", "amount": 2500, "currency": "USD"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Japan budget"