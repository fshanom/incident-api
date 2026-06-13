"""Tests for the DELETE /incidents/{id} endpoint."""

import uuid


def test_delete_incident_returns_204(client, created_incident):
    response = client.delete(f"/incidents/{created_incident['id']}")
    assert response.status_code == 204


def test_delete_incident_removes_it_from_list(client, created_incident):
    client.delete(f"/incidents/{created_incident['id']}")

    response = client.get("/incidents/")

    assert response.json() == []


def test_get_deleted_incident_returns_404(client, created_incident):
    client.delete(f"/incidents/{created_incident['id']}")

    response = client.get(f"/incidents/{created_incident['id']}")

    assert response.status_code == 404


def test_delete_nonexistent_incident_returns_404(client):
    response = client.delete(f"/incidents/{uuid.uuid4()}")
    assert response.status_code == 404
