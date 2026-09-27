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
