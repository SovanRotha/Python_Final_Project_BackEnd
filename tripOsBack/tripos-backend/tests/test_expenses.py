def test_create_expense(client, auth_headers, trip_id, budget_category_id):
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "budget_category_id": budget_category_id,
            "description": "Train ticket",
            "amount": 24.5,
            "currency": "USD",
            "expense_date": "2026-09-28",
        },
    )
    assert response.status_code == 201
    assert float(response.json()["amount"]) == 24.5
