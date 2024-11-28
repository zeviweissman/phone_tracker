from dataclasses import dataclass
from datetime import datetime
from app.db.neo4j_db.models import Device


@dataclass
class Interaction:
    device_1: Device
    device_2: Device
    method: str
    bluetooth_version: str
    signal_strength_dbm: float
    distance_meters: float
    duration_seconds: float
    timestamp: datetime
