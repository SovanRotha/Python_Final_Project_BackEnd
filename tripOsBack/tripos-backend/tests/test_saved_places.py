def test_create_and_list_saved_places(client, auth_headers, destination_id):
    place = client.post(
        "/api/v1/places",
        headers=auth_headers,
        json={
            "destination_id": destination_id,
            "name": "Senso-ji",
            "category": "temple",
        },
    )
    assert place.status_code == 201

    saved = client.post(
        "/api/v1/saved-places",
        headers=auth_headers,
        json={"place_id": place.json()["id"]},
    )
    assert saved.status_code == 201
    assert saved.json()["place_id"] == place.json()["id"]
    assert "user_id" in saved.json()

    duplicate = client.post(
        "/api/v1/saved-places",
        headers=auth_headers,
        json={"place_id": place.json()["id"]},
    )
    assert duplicate.status_code == 409

    listed = client.get("/api/v1/saved-places", headers=auth_headers)
    assert [item["id"] for item in listed.json()] == [saved.json()["id"]]


def test_cannot_save_another_users_place(client, auth_headers, destination_id):
    place = client.post(
        "/api/v1/places",
        headers=auth_headers,
        json={
            "destination_id": destination_id,
            "name": "Senso-ji",
            "category": "temple",
        },
    )
    assert place.status_code == 201

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

    saved = client.post(
        "/api/v1/saved-places",
        headers=other_headers,
        json={"place_id": place.json()["id"]},
    )
    assert saved.status_code == 404
