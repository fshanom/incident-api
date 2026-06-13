"""Endpoints for incident management.

This module keeps incidents in a simple in-memory dictionary (``_incidents``).
There is intentionally no database layer: the goal of this project is to
serve as a study object for a TCC about Infrastructure as Code and container
orchestration, so the application layer is kept as simple as possible.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from app.models.incident import Incident, IncidentCreate, IncidentUpdate, StatusEnum

router = APIRouter(prefix="/incidents", tags=["incidents"])

# In-memory store. Keys are incident IDs, values are Incident instances.
_incidents: Dict[uuid.UUID, Incident] = {}


def _now() -> datetime:
    """Return the current UTC datetime."""

    return datetime.now(timezone.utc)


@router.post("/", response_model=Incident, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate) -> Incident:
    """Create and store a new incident."""

    timestamp = _now()
    incident = Incident(
        id=uuid.uuid4(),
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        status=StatusEnum.open,
        reported_by=payload.reported_by,
        created_at=timestamp,
        updated_at=timestamp,
        resolved_at=None,
        resolution_notes=None,
    )
    _incidents[incident.id] = incident
    return incident


@router.get("/", response_model=List[Incident])
def list_incidents() -> List[Incident]:
    """Return all incidents, most recently created first."""

    return sorted(_incidents.values(), key=lambda incident: incident.created_at, reverse=True)


@router.get("/health/check")
def health_check() -> dict:
    """Return service health information and the total number of incidents."""

    return {
        "status": "healthy",
        "service": "incident-management-api",
        "total_incidents": len(_incidents),
    }


@router.get("/{incident_id}", response_model=Incident)
def get_incident(incident_id: uuid.UUID) -> Incident:
    """Return a single incident by its ID."""

    incident = _incidents.get(incident_id)
    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with id '{incident_id}' not found",
        )
    return incident


@router.put("/{incident_id}", response_model=Incident)
def update_incident(incident_id: uuid.UUID, payload: IncidentUpdate) -> Incident:
    """Update an existing incident.

    When the status is updated to ``resolved`` and ``resolved_at`` has not
    been set yet, it is automatically filled with the current UTC datetime.
    """

    incident = _incidents.get(incident_id)
    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with id '{incident_id}' not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(incident, field, value)

    if incident.status == StatusEnum.resolved and incident.resolved_at is None:
        incident.resolved_at = _now()

    incident.updated_at = _now()

    _incidents[incident_id] = incident
    return incident


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: uuid.UUID) -> None:
    """Remove an incident from the store."""

    if incident_id not in _incidents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with id '{incident_id}' not found",
        )
    del _incidents[incident_id]
