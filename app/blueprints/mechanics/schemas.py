from app.extensions import ma
from app.models import Mechanic
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields


# Define Mechanic Schema
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_fk = True

    # Include service tickets that this mechanic is assigned to
    service_tickets = Nested("ServiceTicketSchema", only=("id", "VIN", "service_date", "service_desc"), many=True)

    # Add validation for email & phone
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=lambda p: len(p) >= 7)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
