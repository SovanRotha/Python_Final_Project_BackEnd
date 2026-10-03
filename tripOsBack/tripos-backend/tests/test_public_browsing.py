def test_guests_can_browse_destinations(client, destination_id):
    listed = client.get("/api/v1/destinations")
    detail = client.get(f"/api/v1/destinations/{destination_id}")

    assert listed.status_code == 200
    assert any(destination["id"] == destination_id for destination in listed.json())
    assert detail.status_code == 200
    assert detail.json()["id"] == destination_id


def test_guests_can_browse_places_but_cannot_create_them(
    client, auth_headers, destination_id
):
    created = client.post(
        "/api/v1/places",
        headers=auth_headers,
        json={
            "destination_id": destination_id,
            "name": "Royal Palace",
            "category": "landmark",
        },
    )
    place_id = created.json()["id"]

    listed = client.get("/api/v1/places")
    detail = client.get(f"/api/v1/places/{place_id}")
    guest_create = client.post(
        "/api/v1/places",
        json={
            "destination_id": destination_id,
            "name": "Wat Phnom",
            "category": "temple",
        },
    )

    assert created.status_code == 201
    assert listed.status_code == 200
    assert any(place["id"] == place_id for place in listed.json())
    assert detail.status_code == 200
    assert detail.json()["id"] == place_id
    assert guest_create.status_code == 401


def test_trip_planning_still_requires_authentication(client):
    response = client.get("/api/v1/trips")

    assert response.status_code == 401
