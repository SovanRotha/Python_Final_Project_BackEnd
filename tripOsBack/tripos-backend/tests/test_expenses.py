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


def test_expense_syncs_trip_wallet_budget_and_transaction(
    client,
    auth_headers,
    trip_id,
    budget_category_id,
):
    wallet = client.post(
        "/api/v1/trip-wallets",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "target_amount": 100,
            "current_amount": 100,
            "currency": "USD",
        },
    )
    assert wallet.status_code == 201, wallet.text
    wallet_id = wallet.json()["id"]

    created = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "budget_category_id": budget_category_id,
            "wallet_id": wallet_id,
            "description": "Train ticket",
            "amount": 24.5,
            "currency": "USD",
            "expense_date": "2026-09-28",
        },
    )
    assert created.status_code == 201, created.text
    expense_id = created.json()["id"]

    transactions = client.get(
        "/api/v1/wallet-transactions",
        headers=auth_headers,
    )
    assert transactions.status_code == 200
    assert len(transactions.json()) == 1
    assert transactions.json()[0]["source"] == f"expense:{expense_id}"
    assert transactions.json()[0]["type"] == "withdrawal"
    budget_after_create = client.get(
        "/api/v1/budgets",
        headers=auth_headers,
    ).json()[0]
    assert float(budget_after_create["spent_amount"]) == 24.5

    updated = client.patch(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers,
        json={"amount": 30},
    )
    assert updated.status_code == 200, updated.text
    budget_after_update = client.get(
        "/api/v1/budgets",
        headers=auth_headers,
    ).json()[0]
    assert float(budget_after_update["spent_amount"]) == 30

    wallet_after_update = client.get(
        f"/api/v1/trip-wallets/{wallet_id}",
        headers=auth_headers,
    )
    assert float(wallet_after_update.json()["current_amount"]) == 70

    deleted = client.delete(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers,
    )
    assert deleted.status_code == 204

    wallet_after_delete = client.get(
        f"/api/v1/trip-wallets/{wallet_id}",
        headers=auth_headers,
    )
    assert float(wallet_after_delete.json()["current_amount"]) == 100
    assert client.get(
        "/api/v1/wallet-transactions",
        headers=auth_headers,
    ).json() == []
    budget_after_delete = client.get(
        "/api/v1/budgets",
        headers=auth_headers,
    ).json()[0]
    assert float(budget_after_delete["spent_amount"]) == 0


def test_expense_rejects_overdraw_without_partial_changes(
    client,
    auth_headers,
    trip_id,
    budget_category_id,
):
    wallet = client.post(
        "/api/v1/trip-wallets",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "target_amount": 10,
            "current_amount": 10,
            "currency": "USD",
        },
    )
    assert wallet.status_code == 201, wallet.text

    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "budget_category_id": budget_category_id,
            "wallet_id": wallet.json()["id"],
            "description": "Over-budget ticket",
            "amount": 11,
            "currency": "USD",
            "expense_date": "2026-09-28",
        },
    )
    assert response.status_code == 422

    refreshed_wallet = client.get(
        f"/api/v1/trip-wallets/{wallet.json()['id']}",
        headers=auth_headers,
    )
    assert float(refreshed_wallet.json()["current_amount"]) == 10
    assert client.get("/api/v1/expenses", headers=auth_headers).json() == []
    assert client.get("/api/v1/wallet-transactions", headers=auth_headers).json() == []
    budget = client.get("/api/v1/budgets", headers=auth_headers).json()[0]
    assert float(budget["spent_amount"]) == 0
