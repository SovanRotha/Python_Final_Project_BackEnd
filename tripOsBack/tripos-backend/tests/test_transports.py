def test_create_and_list_transports(client, auth_headers, trip_id):
    created = client.post(
        "/api/v1/transports",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "type": "bus",
            "provider": "City Bus",
            "from_location": "Phnom Penh",
            "to_location": "Siem Reap",
            "departure_time": "2026-10-10T08:00:00Z",
            "arrival_time": "2026-10-10T14:00:00Z",
        },
    )

    assert created.status_code == 201
    assert created.json()["trip_id"] == trip_id
    assert created.json()["type"] == "bus"
    assert created.json()["provider"] == "City Bus"

    listed = client.get("/api/v1/transports", headers=auth_headers)
    assert [item["id"] for item in listed.json()] == [created.json()["id"]]


def test_cannot_create_transport_for_another_users_trip(
    client, auth_headers, trip_id
):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "other@example.com",
            "password": "secure-pass-456",
            "full_name": "Other Traveler",
        },
    )
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "other@example.com", "password": "secure-pass-456"},
    )
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    created = client.post(
        "/api/v1/transports",
        headers=other_headers,
        json={
            "trip_id": trip_id,
            "type": "bus",
            "from_location": "Phnom Penh",
            "to_location": "Siem Reap",
            "departure_time": "2026-10-10T08:00:00Z",
            "arrival_time": "2026-10-10T14:00:00Z",
        },
    )

    assert created.status_code == 404
