from flask import Blueprint, jsonify, request
import app.db.neo4j_db.service.interaction_service as device_service

phones_blueprint = Blueprint("phones", __name__)

@phones_blueprint.route("/", methods=['POST'])
def receive_interactions():
    device_service.register_interaction_between_devices(request.json)
    return jsonify({}), 200