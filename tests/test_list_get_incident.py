"""Tests for GET /incidents/ and GET /incidents/{id}."""

import time
import uuid


def test_list_incidents_empty_initially(client):
    response = client.get("/incidents/")

    assert response.status_code == 200
    assert response.json() == []


def test_list_incidents_returns_all_created(client, incident_payload):
    client.post("/incidents/", json=incident_payload)
    client.post("/incidents/", json=incident_payload)
    client.post("/incidents/", json=incident_payload)

    response = client.get("/incidents/")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_incidents_ordered_by_most_recent_first(client, incident_payload):
    first_payload = dict(incident_payload, title="Primeiro incidente")
    second_payload = dict(incident_payload, title="Segundo incidente")
    third_payload = dict(incident_payload, title="Terceiro incidente")

    first = client.post("/incidents/", json=first_payload).json()
    time.sleep(0.01)
    second = client.post("/incidents/", json=second_payload).json()
    time.sleep(0.01)
    third = client.post("/incidents/", json=third_payload).json()

    response = client.get("/incidents/")
    incidents = response.json()

    assert [incident["id"] for incident in incidents] == [
        third["id"],
        second["id"],
        first["id"],
    ]


def test_get_incident_by_id_returns_200(client, created_incident):
    response = client.get(f"/incidents/{created_incident['id']}")
    assert response.status_code == 200


def test_get_incident_by_id_returns_correct_data(client, created_incident, incident_payload):
    response = client.get(f"/incidents/{created_incident['id']}")
    data = response.json()

    assert data["id"] == created_incident["id"]
    assert data["title"] == incident_payload["title"]
    assert data["description"] == incident_payload["description"]
    assert data["severity"] == incident_payload["severity"]
    assert data["reported_by"] == incident_payload["reported_by"]


def test_get_nonexistent_incident_returns_404(client):
    response = client.get(f"/incidents/{uuid.uuid4()}")
    assert response.status_code == 404


def test_get_nonexistent_incident_404_has_detail_field(client):
    response = client.get(f"/incidents/{uuid.uuid4()}")
    assert "detail" in response.json()
