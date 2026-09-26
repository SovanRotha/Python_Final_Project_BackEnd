def test_create_and_list_trips(client, auth_headers):
    created = client.post(
        "/api/v1/trips",
        headers=auth_headers,
        json={"name": "Tokyo", "description": "Spring trip", "data": {}},
    )
    assert created.status_code == 201
    assert created.json()["name"] == "Tokyo"

    listed = client.get("/api/v1/trips", headers=auth_headers)
    assert [trip["id"] for trip in listed.json()] == [created.json()["id"]]