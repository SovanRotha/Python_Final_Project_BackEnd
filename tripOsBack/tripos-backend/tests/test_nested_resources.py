def test_create_memory_photo_for_owned_memory(client, auth_headers, trip_id):
    memory = client.post(
        "/api/v1/memories",
        headers=auth_headers,
        json={
            "trip_id": trip_id,
            "title": "Visit to the palace",
            "memory_date": "2026-10-10",
        },
    )
    assert memory.status_code == 201

    photo = client.post(
        "/api/v1/memory-photos",
        headers=auth_headers,
        json={
            "memory_id": memory.json()["id"],
            "image_path": "uploads/palace.jpg",
            "caption": "Royal Palace",
        },
    )

    assert photo.status_code == 201
    assert photo.json()["memory_id"] == memory.json()["id"]
    assert photo.json()["image_path"] == "uploads/palace.jpg"


def test_create_checklist_item_for_owned_checklist(
    client, auth_headers, trip_id
):
    checklist = client.post(
        "/api/v1/checklists",
        headers=auth_headers,
        json={"trip_id": trip_id, "title": "Things to do"},
    )
    assert checklist.status_code == 201

    item = client.post(
        "/api/v1/checklist-items",
        headers=auth_headers,
        json={
            "checklist_id": checklist.json()["id"],
            "title": "Visit Wat Phnom",
            "due_date": "2026-10-10",
        },
    )

    assert item.status_code == 201
    assert item.json()["checklist_id"] == checklist.json()["id"]
    assert item.json()["title"] == "Visit Wat Phnom"
