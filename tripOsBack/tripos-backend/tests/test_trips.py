def test_create_and_list_trips(client, auth_headers, destination_id):
    created = client.post(
        "/api/v1/trips",
        headers=auth_headers,
        json={
            "destination_id": destination_id,
            "name": "Tokyo",
            "description": "Spring trip",
            "start_date": "2026-10-01",
            "end_date": "2026-10-08",
            "currency": "JPY",
        },
    )
    assert created.status_code == 201
    assert created.json()["name"] == "Tokyo"

    listed = client.get("/api/v1/trips", headers=auth_headers)
    assert [trip["id"] for trip in listed.json()] == [created.json()["id"]]


def test_create_trip_with_legacy_amount_status_and_extra_data(
    client, auth_headers, destination_id
):
    created = client.post(
        "/api/v1/trips",
        headers=auth_headers,
        json={
            "destination_id": destination_id,
            "name": "Phnom Penh Weekend Trip",
            "description": "A three-day cultural trip.",
            "data": {"destination": "Phnom Penh", "country": "Cambodia"},
            "start_date": "2026-10-10",
            "end_date": "2026-10-12",
            "status": "planned",
            "amount": 250,
            "balance": 85.5,
            "currency": "USD",
            "category": "Travel",
            "spent_on": "2026-10-10",
            "travelers": 2,
            "transport": "Tuk Tuk",
            "accommodation": "Hotel",
            "places": ["Royal Palace", "Wat Phnom", "Central Market"],
        },
    )

    assert created.status_code == 201
    trip = created.json()
    assert trip["budget_amount"] == "250.00"
    assert trip["status"] == "planning"
    assert trip["data"] == {
        "destination": "Phnom Penh",
        "country": "Cambodia",
        "balance": 85.5,
        "category": "Travel",
        "spent_on": "2026-10-10",
        "travelers": 2,
        "transport": "Tuk Tuk",
        "accommodation": "Hotel",
        "places": ["Royal Palace", "Wat Phnom", "Central Market"],
    }
