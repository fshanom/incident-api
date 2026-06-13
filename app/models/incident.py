"""Pydantic models for the Incident Management API."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SeverityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class StatusEnum(str, Enum):
    open = "open"
    investigating = "investigating"
    resolved = "resolved"
    closed = "closed"


class IncidentCreate(BaseModel):
    """Payload required to register a new incident."""

    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    severity: SeverityEnum
    reported_by: str


class IncidentUpdate(BaseModel):
    """Payload accepted when updating an existing incident.

    All fields are optional so that callers may update only the
    attributes that changed.
    """

    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, min_length=10)
    severity: Optional[SeverityEnum] = None
    status: Optional[StatusEnum] = None
    resolution_notes: Optional[str] = None


class Incident(BaseModel):
    """Full representation of an incident as stored and returned by the API."""

    id: uuid.UUID
    title: str
    description: str
    severity: SeverityEnum
    status: StatusEnum = StatusEnum.open
    reported_by: str
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
