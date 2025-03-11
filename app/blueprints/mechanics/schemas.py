from app.extensions import ma
from app.models import Mechanic
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, ValidationError, validates
from marshmallow.validate import Email


# Define Mechanic Schema
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
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

    # Include service mechanic tickets that this mechanic is assigned to
    mechanic_tickets = Nested("ServiceMechanicSchema", only=("service_ticket_id", 
                                                             "service_ticket.VIN", 
                                                             "service_ticket.service_date", 
                                                             "service_ticket.service_desc"), 
                                                             many=True, required=False)

    def __init__(self, *args, **kwargs):
        from app.blueprints.serviceMechanics.schemas import ServiceMechanicSchema

        self.mechanic_tickets = Nested(ServiceMechanicSchema, only=("service_ticket_id", 
                                                                    "service_ticket.VIN",
                                                                   "service_ticket.service_date", 
                                                                   "service_ticket.service_desc"), 
                                                                   many=True, required=False)

        super().__init__(*args, **kwargs)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
