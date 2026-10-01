def test_create_and_list_checklists(client, auth_headers, trip_id):
    created = client.post(
        "/api/v1/checklists",
        headers=auth_headers,
        json={"trip_id": trip_id, "title": "Packing checklist"},
    )

    assert created.status_code == 201
    assert created.json()["trip_id"] == trip_id
    assert created.json()["title"] == "Packing checklist"

    listed = client.get("/api/v1/checklists", headers=auth_headers)
    assert [checklist["id"] for checklist in listed.json()] == [created.json()["id"]]


def test_cannot_create_checklist_for_another_users_trip(
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
        "/api/v1/checklists",
        headers=other_headers,
        json={"trip_id": trip_id, "title": "Unauthorized checklist"},
    )

    assert created.status_code == 404
