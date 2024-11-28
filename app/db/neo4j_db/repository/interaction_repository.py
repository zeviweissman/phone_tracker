from dataclasses import asdict
from app.db.neo4j_db.crud import merge, data_query
from app.db.neo4j_db.models import Interaction
import app.utils.convert_utils as convert_utils
from returns.maybe import Maybe


def create_interaction(interaction: Interaction):
    device_one_params = convert_utils.device_params_from_device(interaction.device_1)
    device_two_params = convert_utils.device_params_from_device(interaction.device_2)
    rel_params = {
        "method": interaction.method,
        "bluetooth_version": interaction.bluetooth_version,
        "signal_strength_dbm": interaction.signal_strength_dbm,
        "distance_meters": interaction.distance_meters,
        "duration_seconds": interaction.duration_seconds,
        "timestamp": interaction.timestamp
    }
    labels=['Device']
    rel = "CALLED"

    res = merge(
        node_one_params=device_one_params,
        node_one_labels=labels,
        node_two_params=device_two_params,
        node_two_labels=labels,
        rel=rel,
        rel_params=rel_params
    )
    return (Maybe.from_optional(res.get("rel"))
            .map(lambda rel: dict(rel)))


def get_bluetooth_path():
    query = """
            MATCH (start:Device)
            MATCH (end:Device)
            WHERE start <> end
            MATCH path = shortestPath((start)-[:CALLED*]->(end))
            WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
            WITH path, length(path) as pathLength
            ORDER BY pathLength DESC
            RETURN length(path), path
            """
    return data_query(query=query)


def get_devices_with_strong_signal():
    query = """
            MATCH  (d1:Device)-[rel:CALLED]->(d2:Device)
            WHERE rel.signal_strength_dbm > -60
            RETURN [d1, d2]
            """
    return data_query(query=query)


def get_interaction_count_by_id(id: str):
    query = """
        MATCH  devices = (:Device{id:$id})-[:CALLED]->(:Device)
        RETURN count(devices)
            """
    params = {"id": id}
    return data_query(query=query, params=params)


def check_if_two_devices_have_interaction(id1: str, id2: str):
    query = """
            MATCH (n1:Device {id: $id1}), (n2:Device {id: $id2})
            RETURN EXISTS((n1)-[:CALLED]-(n2))  as have_connection
                """
    params = {"id1": id1, "id2": id2}
    return data_query(query=query, params=params)