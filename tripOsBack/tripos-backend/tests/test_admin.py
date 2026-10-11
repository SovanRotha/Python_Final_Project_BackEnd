from app.core.config import settings


def register_and_login(client, email, name):
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "secure-pass-123", "name": name},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "secure-pass-123"},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_admin_api_rejects_non_admin_users(client, auth_headers):
    response = client.get("/api/v1/admin/dashboard", headers=auth_headers)

    assert response.status_code == 403


def test_admin_management_and_report_workflow(client, monkeypatch):
    monkeypatch.setattr(settings, "ADMIN_EMAILS", "admin@example.com")
    admin_headers = register_and_login(client, "admin@example.com", "Admin")
    user_headers = register_and_login(client, "traveler@example.com", "Traveler")

    report = client.post(
        "/api/v1/reports",
        headers=user_headers,
        json={
            "reason": "Incorrect information",
            "description": "The opening hours are out of date.",
            "resource_type": "place",
            "resource_id": 7,
        },
    )
    assert report.status_code == 201

    destination = client.post(
        "/api/v1/destinations",
        headers=user_headers,
        json={
            "name": "Kyoto",
            "country": "Japan",
            "country_code": "JP",
            "currency": "JPY",
            "language": "Japanese",
            "best_time": "Spring and autumn",
        },
    )
    assert destination.status_code == 201
    destination_id = destination.json()["id"]

    updated_destination = client.patch(
        f"/api/v1/destinations/{destination_id}",
        headers=admin_headers,
        json={"description": "Admin-maintained destination information."},
    )
    assert updated_destination.status_code == 200
    assert (
        updated_destination.json()["description"]
        == "Admin-maintained destination information."
    )

    place = client.post(
        "/api/v1/places",
        headers=admin_headers,
        json={
            "destination_id": destination_id,
            "name": "Kiyomizu-dera",
            "category": "temple",
            "rating": 4.8,
        },
    )
    assert place.status_code == 201

    updated_place = client.patch(
        f"/api/v1/places/{place.json()['id']}",
        headers=admin_headers,
        json={"status": "inactive"},
    )
    assert updated_place.status_code == 200
    assert updated_place.json()["status"] == "inactive"
    destination_list = client.get("/api/v1/destinations").json()
    assert any(item["id"] == destination_id for item in destination_list)
    place_list = client.get("/api/v1/places").json()
    assert any(item["id"] == place.json()["id"] for item in place_list)

    user_list = client.get("/api/v1/admin/users", headers=admin_headers).json()
    traveler = next(item for item in user_list["items"] if item["name"] == "Traveler")
    assert "hashed_password" not in traveler
    suspended = client.patch(
        f"/api/v1/admin/users/{traveler['id']}",
        headers=admin_headers,
        json={"status": False},
    )
    assert suspended.status_code == 200
    assert suspended.json()["status"] is False
    assert client.get("/api/v1/users/me", headers=user_headers).status_code == 401

    reports = client.get("/api/v1/admin/reports", headers=admin_headers).json()
    assert reports["items"][0]["status"] == "open"
    reviewed = client.patch(
        f"/api/v1/admin/reports/{report.json()['id']}",
        headers=admin_headers,
        json={"status": "resolved", "resolution": "Updated the hours."},
    )
    assert reviewed.status_code == 200
    assert reviewed.json()["reviewed_by_id"] == 1

    dashboard = client.get("/api/v1/admin/dashboard", headers=admin_headers).json()
    assert dashboard["statistics"]["users"] == 2
    assert dashboard["statistics"]["destinations"] == 1
    assert dashboard["statistics"]["places"] == 1
    assert dashboard["statistics"]["open_reports"] == 0
    logs = client.get("/api/v1/admin/audit-logs", headers=admin_headers).json()
    assert {item["action"] for item in logs["items"]} >= {
        "destination_updated",
        "place_created",
        "place_updated",
        "user_status_updated",
        "report_reviewed",
    }


def test_allowlisted_admin_cannot_suspend_self(client, monkeypatch):
    monkeypatch.setattr(settings, "ADMIN_EMAILS", "admin@example.com")
    admin_headers = register_and_login(client, "admin@example.com", "Admin")

    response = client.patch(
        "/api/v1/admin/users/1",
        headers=admin_headers,
        json={"status": False},
    )

    assert response.status_code == 409
