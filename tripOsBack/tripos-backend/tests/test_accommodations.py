def test_create_and_list_accommodations(client, auth_headers, trip_id):
    created = client.post(
        "/api/v1/accommodations",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "name": "Riverside Hotel",
            "check_in": "2026-10-10T15:00:00",
            "check_out": "2026-10-12T11:00:00",
            "room_type": "Standard",
        },
    )

    assert created.status_code == 201
    assert created.json()["trip_id"] == trip_id
    assert created.json()["name"] == "Riverside Hotel"

    listed = client.get("/api/v1/accommodations", headers=auth_headers)
    assert [item["id"] for item in listed.json()] == [created.json()["id"]]


def test_cannot_create_accommodation_for_another_users_trip(
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
        "/api/v1/accommodations",
        headers=other_headers,
        json={
            "trip_id": trip_id,
            "name": "Unauthorized booking",
            "check_in": "2026-10-10T15:00:00",
            "check_out": "2026-10-12T11:00:00",
        },
    )

    assert created.status_code == 404
