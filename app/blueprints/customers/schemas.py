from app.extensions import ma
from app.models import Customer
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Email


# Define Customer Schema
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True

    # Add validation for name, email & phone
    email = fields.Email(required=True, validate=Email())
    @validates('email')
    def validate_email(self, value):
        if not value:
            raise ValidationError("Email is required.")
        if '@' not in value:
            raise ValidationError("Invalid email address.")
        
        
    phone = fields.String(required=True, validate=lambda p: len(p) >= 7)

    # Include customer's service tickets
    service_tickets = Nested("ServiceTicketSchema", only=("id", 
                                                          "VIN", 
                                                          "service_date", 
                                                          "service_desc"), 
                                                          many=True, required=False)


    def __init__(self, *args, **kwargs):
        from app.blueprints.serviceTickets.schemas import ServiceTicketSchema

        self.service_tickets = Nested(ServiceTicketSchema, only=("id", 
                                                                 "VIN", 
                                                                 "service_date", 
                                                                 "service_desc"), 
                                                                 many=True, required=False)

        super().__init__(*args, **kwargs)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
