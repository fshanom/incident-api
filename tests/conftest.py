"""Shared pytest fixtures for the Incident Management API test suite."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.incidents import _incidents


@pytest.fixture(autouse=True)
def clear_store():
    """Ensure the in-memory incident store is empty before and after each test."""

    _incidents.clear()
    yield
    _incidents.clear()


@pytest.fixture
def client():
    """Return a TestClient instance for the FastAPI application."""

    return TestClient(app)


@pytest.fixture
def incident_payload():
    """Return a valid payload describing a real-world incident."""

    return {
        "title": "Falha no serviço de pagamentos",
        "description": "O serviço de pagamentos está retornando erro 500 para todas as transações.",
        "severity": "high",
        "reported_by": "ops-team",
    }


@pytest.fixture
def created_incident(client, incident_payload):
    """Create an incident via the API and return the resulting JSON body."""

    response = client.post("/incidents/", json=incident_payload)
    return response.json()
