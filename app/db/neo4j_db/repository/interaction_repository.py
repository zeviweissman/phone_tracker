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
            match path = (:Device) -[:CALLED*{method:"Bluetooth"}] -> (:Device)
            return length(path), path
            """
    return data_query(query=query)
