from dataclasses import asdict
from app.db.neo4j_db.crud import recreate, read_all
from app.db.neo4j_db.models import Location
from returns.maybe import Maybe


def get_all_locations():
    return read_all(labels=['Location'])



def recreate_location(location: Location):
    res = recreate(labels=['Location'], params=location)
    return (Maybe.from_optional(res.get("o"))
                .map(lambda u: dict(u)))
