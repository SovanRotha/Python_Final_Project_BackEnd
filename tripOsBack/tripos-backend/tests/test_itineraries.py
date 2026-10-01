def test_create_itinerary_with_dates_and_details(client, auth_headers):
    created = client.post(
        "/api/v1/itineraries",
        headers=auth_headers,
        json={
            "name": "Phnom Penh Weekend Trip",
            "description": "A three-day cultural trip.",
            "data": {"destination": "Phnom Penh"},
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
    assert created.json()["name"] == "Phnom Penh Weekend Trip"
    assert created.json()["data"] == {
        "destination": "Phnom Penh",
        "start_date": "2026-10-10",
        "end_date": "2026-10-12",
        "status": "planned",
        "amount": 250,
        "balance": 85.5,
        "currency": "USD",
        "category": "Travel",
        "spent_on": "2026-10-10",
    }
