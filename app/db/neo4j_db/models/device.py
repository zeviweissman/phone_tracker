from dataclasses import dataclass
from app.db.neo4j_db.models import Location


@dataclass
class Device:
    id: str
    brand: str
    model: str
    os: str
    name: str
    location: Location
