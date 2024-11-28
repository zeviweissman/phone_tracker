from dataclasses import asdict
from app.db.neo4j_db.crud import create, read_all, read_one, merge
from app.db.neo4j_db.models import Device
from returns.maybe import Maybe
import app.utils.convert_utils as convert_utils




def get_all_devices():
    return read_all(labels=['Device'])


def get_one_device(device: Device):
    params = convert_utils.device_params_from_device(device)
    return read_one(labels=['Device'], params=params)

def create_device(device: Device):
    params = convert_utils.device_params_from_device(device)
    res = create(labels=['Device'], params=params)
    return (Maybe.from_optional(res.get("o"))
                .map(lambda u: dict(u)))


def merge_device_with_location(device: Device):
    device_params = convert_utils.device_params_from_device(device)
    location_params = device.location
    res = merge(
        node_one_params=device_params,
        node_one_labels=['Device'],
        node_two_params=location_params,
        node_two_labels=['Location'],
        rel="IS_IN_LOCATION",
        rel_params={}
    )
    return (Maybe.from_optional(res.get("rel"))
            .map(lambda rel: dict(rel)))