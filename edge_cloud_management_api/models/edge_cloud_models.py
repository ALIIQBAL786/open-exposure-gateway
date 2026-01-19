from typing import Optional
from pydantic import BaseModel, UUID4
from enum import Enum


class EdgeCloudZoneStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    unknown = "unknown"


class EdgeCloudZone(BaseModel):
    edgeCloudZoneId: UUID4
    edgeCloudZoneName: str
    edgeCloudZoneStatus: Optional[EdgeCloudZoneStatus]
    edgeCloudProvider: str
    edgeCloudRegion: Optional[str]

