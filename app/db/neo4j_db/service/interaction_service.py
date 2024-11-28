from typing import List
import app.utils.convert_utils as convert_utils
import app.db.neo4j_db.repository.interaction_repository as interaction_repos
import app.db.neo4j_db.repository.device_repository as device_repos
import app.db.neo4j_db.repository.location_repository as location_repos
from app.db.neo4j_db.models import Device


def merge_device_with_location(device: Device):
    location_repos.recreate_location(device.location)
    device_repos.create_device(device)
    device_repos.merge_device_with_location(device)

def register_interaction_between_devices(interaction):
    parsed_interaction = convert_utils.interaction_json_to_interaction_model(interaction)
    if not device_repos.get_one_device(parsed_interaction.device_1):
        merge_device_with_location(parsed_interaction.device_1)
    if not device_repos.get_one_device(parsed_interaction.device_2):
        merge_device_with_location(parsed_interaction.device_2)
    interaction_repos.create_interaction(parsed_interaction)


def get_bluetooth_path():
    return interaction_repos.get_bluetooth_path()


def get_devices_with_strong_signal():
    return interaction_repos.get_devices_with_strong_signal()


def get_interaction_count_by_id(id: str):
    return interaction_repos.get_interaction_count_by_id(id)


def check_if_two_devices_have_interaction(id1: str, id2: str):
    return interaction_repos.check_if_two_devices_have_interaction(id1, id2)