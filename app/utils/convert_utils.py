import toolz as t
from app.db.neo4j_db.models import Interaction, Device


def device_json_to_device_model(device: dict):
    return Device(**device)


def interaction_json_to_interaction_model(interaction: dict):
    return Interaction(
        device_1=device_json_to_device_model(t.get_in(['devices', 0], interaction)),
        device_2=device_json_to_device_model(t.get_in(['devices', 1], interaction)),
        method=t.get_in(['interaction', 'method'], interaction),
        distance_meters=t.get_in(['interaction', 'distance_meters'], interaction),
        bluetooth_version=t.get_in(['interaction', 'bluetooth_version'], interaction),
        signal_strength_dbm=t.get_in(['interaction', 'signal_strength_dbm'], interaction),
        duration_seconds=t.get_in(['interaction', 'duration_seconds'], interaction),
        timestamp=t.get_in(['interaction', 'timestamp'], interaction)
    )


def device_params_from_device(device: Device):
    return {
        "id": device.id,
        "model": device.model,
        "os": device.os,
        "brand": device.brand,
        "name": device.name
    }