"""Tests for the PUT /incidents/{id} endpoint."""

import time
import uuid


def test_update_incident_status(client, created_incident):
    response = client.put(
        f"/incidents/{created_incident['id']}",
        json={"status": "investigating"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "investigating"


def test_update_incident_severity(client, created_incident):
    response = client.put(
        f"/incidents/{created_incident['id']}",
        json={"severity": "critical"},
    )

    assert response.status_code == 200
    assert response.json()["severity"] == "critical"


def test_update_incident_title(client, created_incident):
    response = client.put(
        f"/incidents/{created_incident['id']}",
        json={"title": "Título atualizado do incidente"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Título atualizado do incidente"


def test_resolve_incident_sets_resolved_at_automatically(client, created_incident):
    assert created_incident["resolved_at"] is None

    response = client.put(
        f"/incidents/{created_incident['id']}",
        json={"status": "resolved"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"
    assert response.json()["resolved_at"] is not None


def test_resolve_incident_saves_resolution_notes(client, created_incident):
    response = client.put(
        f"/incidents/{created_incident['id']}",
        json={"status": "resolved", "resolution_notes": "Reiniciado o serviço de pagamentos."},
    )

    assert response.status_code == 200
    assert response.json()["resolution_notes"] == "Reiniciado o serviço de pagamentos."


def test_update_incident_changes_updated_at(client, created_incident):
    original_updated_at = created_incident["updated_at"]

    time.sleep(0.01)
    response = client.put(
        f"/incidents/{created_incident['id']}",
        json={"title": "Novo título para forçar atualização"},
    )

    assert response.status_code == 200
    assert response.json()["updated_at"] != original_updated_at


def test_update_nonexistent_incident_returns_404(client):
    response = client.put(
        f"/incidents/{uuid.uuid4()}",
        json={"title": "Não importa"},
    )

    assert response.status_code == 404


def test_update_incident_invalid_status_returns_422(client, created_incident):
    response = client.put(
        f"/incidents/{created_incident['id']}",
        json={"status": "not-a-valid-status"},
    )

    assert response.status_code == 422


def test_incident_full_lifecycle_open_to_closed(client, created_incident):
    """Exercita o ciclo de vida completo de um incidente.

    O ciclo open -> investigating -> resolved -> closed é utilizado no TCC
    para calcular o MTTR (Mean Time To Recovery): o intervalo entre
    created_at (abertura do incidente) e resolved_at (momento em que ele
    foi marcado como resolvido).
    """

    incident_id = created_incident["id"]
    assert created_incident["status"] == "open"

    investigating = client.put(
        f"/incidents/{incident_id}",
        json={"status": "investigating"},
    )
    assert investigating.json()["status"] == "investigating"
    assert investigating.json()["resolved_at"] is None

    resolved = client.put(
        f"/incidents/{incident_id}",
        json={
            "status": "resolved",
            "resolution_notes": "Causa raiz identificada e corrigida; serviço normalizado.",
        },
    )
    assert resolved.json()["status"] == "resolved"
    assert resolved.json()["resolved_at"] is not None
    assert (
        resolved.json()["resolution_notes"]
        == "Causa raiz identificada e corrigida; serviço normalizado."
    )

    resolved_at_after_resolution = resolved.json()["resolved_at"]

    closed = client.put(
        f"/incidents/{incident_id}",
        json={"status": "closed"},
    )
    assert closed.json()["status"] == "closed"
    assert closed.json()["resolved_at"] == resolved_at_after_resolution
    assert (
        closed.json()["resolution_notes"]
        == "Causa raiz identificada e corrigida; serviço normalizado."
    )
