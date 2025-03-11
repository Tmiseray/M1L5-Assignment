from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db
from . import service_tickets_bp
from app.models import ServiceTicket, ServiceMechanic, Mechanic
from .schemas import service_ticket_schema, service_tickets_schema


# Create service_ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_service_ticket = ServiceTicket(
        VIN=service_ticket_data['VIN'],
        service_date=service_ticket_data['service_date'],
        service_desc=service_ticket_data['service_desc'],
        customer_id=service_ticket_data['customer_id']
    )

    # Add mechanics (Many-to-Many via ServiceMechanic)
    for mechanic_id in service_ticket_data['mechanic_ids']:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic:
            new_service_ticket.service_mechanics.append(ServiceMechanic(mechanic=mechanic))

    db.session.add(new_service_ticket)
    db.session.commit()

    return jsonify(service_ticket_schema.dump(new_service_ticket)), 201


# Get all service_tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    result = db.session.execute(query).scalars().all()
    return jsonify(service_tickets_schema.dump(result)), 200


# Get single service_ticket
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if service_ticket is None:
        return jsonify({"message": "Invalid service_ticket ID"}), 404

    return jsonify(service_ticket_schema.dump(service_ticket)), 200


# Update a service_ticket
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if service_ticket is None:
        return jsonify({"message": "Invalid service_ticket ID"}), 404

    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Update basic fields
    service_ticket.VIN = service_ticket_data['VIN']
    service_ticket.service_date = service_ticket_data['service_date']
    service_ticket.service_desc = service_ticket_data['service_desc']
    service_ticket.customer_id = service_ticket_data['customer_id']

    # Update mechanics (Clear & Re-add)
    service_ticket.service_mechanics.clear()
    for mechanic_id in service_ticket_data['mechanic_ids']:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic:
            service_ticket.service_mechanics.append(ServiceMechanic(mechanic=mechanic))

    db.session.commit()

    return jsonify(service_ticket_schema.dump(service_ticket)), 200


# Delete a service_ticket
@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if service_ticket is None:
        return jsonify({"message": "Invalid service_ticket ID"}), 404

    db.session.delete(service_ticket)
    db.session.commit()

    return jsonify({"message": "Service ticket deleted"}), 200
