def test_create_expense(client, auth_headers):
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={"name": "Train ticket", "amount": 24.5, "currency": "USD", "category": "transport"},
    )
    assert response.status_code == 201
    assert response.json()["amount"] == 24.5