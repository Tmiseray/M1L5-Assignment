
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select, delete
from . import customers_bp
from app.models import Customer, db
from .schemas import customer_schema, customers_schema, customer_login_schema
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required


# Customer Login
@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = customer_login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting email and password'}), 400
    
    query = select(Customer).where(Customer.email == email) 
    customer = db.session.execute(query).scalar_one_or_none() 

    if customer and customer.password == password: 
        auth_token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': "Invalid email or password"}), 401


# Create Customer
@customers_bp.route('/', methods=['POST'])
@limiter.limit("3 per hour")
# Limit the number of customer creations to 3 per hour
# There shouldn't be a need to create more than 3 customers per hour
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_customer = Customer(
        name=customer_data['name'],
        email=customer_data['email'],
        phone=customer_data['phone'],
        password=customer_data['password']
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify(customer_schema.dump(new_customer)), 201


# Get all customers
@customers_bp.route('/', methods=['GET'])
@limiter.limit("10 per hour")
# Limit the number of retrievals to 10 per hour
# There shouldn't be a need to retrieve all customers more than 10 per hour
@cache.cached(timeout=60)
# Cache the response for 60 seconds
# This will help reduce the load on the database
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars().all()
    return jsonify(customers_schema.dump(result)), 200


# Get single customer
@customers_bp.route('/<int:customer_id>', methods=['GET'])
@limiter.limit("10 per hour")
# Limit the number of retrievals to 10 per hour
# There shouldn't be a need to retrieve a single customer more than 10 per hour
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"message": "Invalid customer ID"}), 404

    return jsonify(customer_schema.dump(customer)), 200


# Update a customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"message": "Invalid customer ID"}), 404

    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    customer.name = customer_data.get('name') or customer.name
    customer.email = customer_data.get('email') or customer.email
    customer.phone = customer_data.get('phone') or customer.phone

    db.session.commit()

    return jsonify(customer_schema.dump(customer)), 200


# Delete a customer
@customers_bp.route('/', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"message": "Invalid customer ID"}), 404

    # Set customer_id to NULL for related service tickets
    for service_ticket in customer.service_tickets:
        service_ticket.customer_id = None

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted"}), 200


# Get customer's service tickets
@customers_bp.route('/my-service-tickets', methods=['GET'])
@limiter.limit("10 per hour")
# Limit the number of retrievals to 10 per hour
# There shouldn't be a need to retrieve a customer's service tickets more than 10 per hour
@token_required
def get_my_service_tickets(current_customer):
    query = select(Customer).where(Customer.id == current_customer.id)
    customer = db.session.execute(query).scalar_one_or_none()

    service_tickets = customer.service_tickets
    return jsonify(customer_schema.dump(service_tickets)), 200