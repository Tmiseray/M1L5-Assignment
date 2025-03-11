from app.extensions import ma
from app.models import Customer
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields


# Define Customer Schema
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True

    # Include customer's service tickets
    service_tickets = Nested("ServiceTicketSchema", only=("id", "VIN", "service_date", "service_desc"), many=True)

    # Add validation for email & phone
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=lambda p: len(p) >= 7)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
