def test_create_wallet_stores_unmapped_fields_in_data(client, auth_headers):
    created = client.post(
        "/api/v1/wallets",
        headers=auth_headers,
        json={
            "name": "Travel wallet",
            "start_date": "2026-10-10",
            "end_date": "2026-10-12",
            "status": "planned",
            "amount": 250,
            "balance": 85.5,
            "currency": "USD",
            "category": "Travel",
            "spent_on": "2026-10-10",
        },
    )

    assert created.status_code == 201
    assert created.json()["balance"] == "85.5"
    assert created.json()["currency"] == "USD"
    assert created.json()["data"] == {
        "start_date": "2026-10-10",
        "end_date": "2026-10-12",
        "status": "planned",
        "amount": 250,
        "category": "Travel",
        "spent_on": "2026-10-10",
    }
