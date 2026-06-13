"""Tests for the GET /incidents/health/check endpoint."""


def test_health_check_returns_200(client):
    response = client.get("/incidents/health/check")
    assert response.status_code == 200


def test_health_check_status_is_healthy(client):
    response = client.get("/incidents/health/check")
    assert response.json()["status"] == "healthy"


def test_health_check_service_name(client):
    response = client.get("/incidents/health/check")
    assert response.json()["service"] == "incident-management-api"


def test_health_check_total_incidents_starts_at_zero(client):
    response = client.get("/incidents/health/check")
    assert response.json()["total_incidents"] == 0


def test_health_check_reflects_real_count_after_creations(client, incident_payload):
    client.post("/incidents/", json=incident_payload)
    client.post("/incidents/", json=incident_payload)
    client.post("/incidents/", json=incident_payload)

    response = client.get("/incidents/health/check")

    assert response.json()["total_incidents"] == 3
