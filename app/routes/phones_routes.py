from flask import Blueprint, jsonify, request
import app.db.neo4j_db.service.interaction_service as interaction_service

phones_blueprint = Blueprint("phones", __name__)

@phones_blueprint.route("/", methods=['POST'])
def receive_interactions():
    interaction_service.register_interaction_between_devices(request.json)
    return jsonify({}), 200


@phones_blueprint.route("/bluetooth_path", methods=['GET'])
def get_bluetooth_path():
    path = interaction_service.get_bluetooth_path()
    return jsonify(path), 200


@phones_blueprint.route("/strong_signal", methods=['GET'])
def get_devices_with_strong_signal():
    path = interaction_service.get_devices_with_strong_signal()
    return jsonify(path), 200