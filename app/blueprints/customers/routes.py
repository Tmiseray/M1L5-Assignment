
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db
from . import customers_bp
from app.models import Customer
from .schemas import customer_schema, customers_schema


# Create Customer
@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_customer = Customer(
        name=customer_data['name'],
        email=customer_data['email'],
        phone=customer_data['phone']
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify(customer_schema.dump(new_customer)), 201


# Get all customers
@customers_bp.route('/', methods=['GET'])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars().all()
    return jsonify(customers_schema.dump(result)), 200


# Get single customer
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"message": "Invalid customer ID"}), 404

    return jsonify(customer_schema.dump(customer)), 200


# Update a customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"message": "Invalid customer ID"}), 404

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']

    db.session.commit()

    return jsonify(customer_schema.dump(customer)), 200


# Delete a customer
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"message": "Invalid customer ID"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200