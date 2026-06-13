"""Tests for the POST /incidents/ endpoint."""


def test_create_incident_returns_201(client, incident_payload):
    response = client.post("/incidents/", json=incident_payload)
    assert response.status_code == 201


def test_create_incident_returns_correct_title(client, incident_payload):
    response = client.post("/incidents/", json=incident_payload)
    assert response.json()["title"] == incident_payload["title"]


def test_create_incident_initial_status_is_open(client, incident_payload):
    response = client.post("/incidents/", json=incident_payload)
    assert response.json()["status"] == "open"


def test_create_incident_ids_are_unique(client, incident_payload):
    first = client.post("/incidents/", json=incident_payload)
    second = client.post("/incidents/", json=incident_payload)

    assert first.json()["id"] != second.json()["id"]


def test_create_incident_returns_correct_reported_by(client, incident_payload):
    response = client.post("/incidents/", json=incident_payload)
    assert response.json()["reported_by"] == incident_payload["reported_by"]


def test_create_incident_accepts_critical_severity(client, incident_payload):
    incident_payload["severity"] = "critical"

    response = client.post("/incidents/", json=incident_payload)

    assert response.status_code == 201
    assert response.json()["severity"] == "critical"


def test_create_incident_missing_title_returns_422(client, incident_payload):
    del incident_payload["title"]

    response = client.post("/incidents/", json=incident_payload)

    assert response.status_code == 422


def test_create_incident_short_title_returns_422(client, incident_payload):
    incident_payload["title"] = "ab"

    response = client.post("/incidents/", json=incident_payload)

    assert response.status_code == 422


def test_create_incident_invalid_severity_returns_422(client, incident_payload):
    incident_payload["severity"] = "super-critical"

    response = client.post("/incidents/", json=incident_payload)

    assert response.status_code == 422


def test_create_incident_short_description_returns_422(client, incident_payload):
    incident_payload["description"] = "too short"

    response = client.post("/incidents/", json=incident_payload)

    assert response.status_code == 422


def test_create_incident_created_at_is_present(client, incident_payload):
    response = client.post("/incidents/", json=incident_payload)
    assert response.json()["created_at"] is not None


def test_create_incident_resolved_at_is_initially_null(client, incident_payload):
    response = client.post("/incidents/", json=incident_payload)
    assert response.json()["resolved_at"] is None
