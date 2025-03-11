
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import mechanics_bp
from app.models import Mechanic, db
from .schemas import mechanic_schema, mechanics_schema


# Create Mechanic
@mechanics_bp.route('/', methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanic(
        name=mechanic_data['name'],
        email=mechanic_data['email'],
        phone=mechanic_data['phone'],
        salary=mechanic_data['salary'] 
    )

    db.session.add(new_mechanic)
    db.session.commit()

    return jsonify(mechanic_schema.dump(new_mechanic)), 201


# Get all mechanics
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    result = db.session.execute(query).scalars().all()
    return jsonify(mechanics_schema.dump(result)), 200


# Get single mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Invalid mechanic ID"}), 404

    return jsonify(mechanic_schema.dump(mechanic)), 200


# Update a mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Invalid mechanic ID"}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    mechanic.name = mechanic_data.get('name') or mechanic.name
    mechanic.email = mechanic_data.get('email') or mechanic.email
    mechanic.phone = mechanic_data.get('phone') or mechanic.phone
    mechanic.salary = mechanic_data.get('salary') or mechanic.salary

    db.session.commit()

    return jsonify(mechanic_schema.dump(mechanic)), 200


# Delete a mechanic
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"message": "Invalid mechanic ID"}), 404

    # Set mechanic_id to NULL for related service mechanics
    for service_mechanic in mechanic.mechanic_tickets:
        service_mechanic.mechanic_id = None

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": "Mechanic deleted"}), 200