from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db
from . import service_mechanics_bp
from app.models import ServiceMechanic, ServiceTicket, Mechanic
from .schemas import service_mechanic_schema, service_mechanics_schema


# Create service_mechanic (Assign a Mechanic to a Service Ticket)
@service_mechanics_bp.route('/', methods=['POST'])
def create_service_mechanic():
    try:
        service_mechanic_data = service_mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check if the service_ticket and mechanic exist
    service_ticket = db.session.get(ServiceTicket, service_mechanic_data['service_ticket_id'])
    mechanic = db.session.get(Mechanic, service_mechanic_data['mechanic_id'])

    if not service_ticket or not mechanic:
        return jsonify({"message": "Invalid service_ticket_id or mechanic_id"}), 400

    # Ensure the relationship doesn't already exist
    existing_entry = db.session.get(ServiceMechanic, (service_mechanic_data['service_ticket_id'], service_mechanic_data['mechanic_id']))
    if existing_entry:
        return jsonify({"message": "Mechanic is already assigned to this service ticket"}), 400

    new_service_mechanic = ServiceMechanic(
        service_ticket_id=service_mechanic_data['service_ticket_id'],
        mechanic_id=service_mechanic_data['mechanic_id']
    )

    db.session.add(new_service_mechanic)
    db.session.commit()

    return jsonify(service_mechanic_schema.dump(new_service_mechanic)), 201


# Get all service_mechanics (List of Assignments)
@service_mechanics_bp.route('/', methods=['GET'])
def get_service_mechanics():
    query = select(ServiceMechanic)
    result = db.session.execute(query).scalars().all()
    return jsonify(service_mechanics_schema.dump(result)), 200


# Get single service_mechanic (By Composite Key)
@service_mechanics_bp.route('/<int:service_ticket_id>/<int:mechanic_id>', methods=['GET'])
def get_service_mechanic(service_ticket_id, mechanic_id):
    service_mechanic = db.session.get(ServiceMechanic, (service_ticket_id, mechanic_id))

    if not service_mechanic:
        return jsonify({"message": "Invalid service_ticket_id or mechanic_id"}), 404

    return jsonify(service_mechanic_schema.dump(service_mechanic)), 200


# Delete a service_mechanic (Remove Mechanic from Service Ticket)
@service_mechanics_bp.route('/<int:service_ticket_id>/<int:mechanic_id>', methods=['DELETE'])
def delete_service_mechanic(service_ticket_id, mechanic_id):
    service_mechanic = db.session.get(ServiceMechanic, (service_ticket_id, mechanic_id))

    if not service_mechanic:
        return jsonify({"message": "Invalid service_ticket_id or mechanic_id"}), 404

    db.session.delete(service_mechanic)
    db.session.commit()

    return jsonify({"message": "ServiceMechanic relationship deleted"}), 200


# DELETE the existing relationship and create a new one.
@service_mechanics_bp.route('/<int:service_ticket_id>/<int:mechanic_id>', methods=['PUT'])
def update_service_mechanic(service_ticket_id, mechanic_id):
    service_mechanic = db.session.get(ServiceMechanic, (service_ticket_id, mechanic_id))

    if not service_mechanic:
        return jsonify({"message": "Invalid service_ticket_id or mechanic_id"}), 404

    try:
        service_mechanic_data = service_mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Delete old entry
    db.session.delete(service_mechanic)

    # Create a new entry
    new_service_mechanic = ServiceMechanic(
        service_ticket_id=service_mechanic_data['service_ticket_id'],
        mechanic_id=service_mechanic_data['mechanic_id']
    )

    db.session.add(new_service_mechanic)
    db.session.commit()

    return jsonify(service_mechanic_schema.dump(new_service_mechanic)), 200
