def test_create_budget(client, auth_headers, trip_id):
    response = client.post(
        "/api/v1/budgets",
        headers=auth_headers,
        json={"trip_id": trip_id, "total_budget": 2500, "currency": "USD"},
    )
    assert response.status_code == 201
    assert float(response.json()["total_budget"]) == 2500
