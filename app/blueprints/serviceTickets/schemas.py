from app.extensions import ma
from app.models import ServiceTicket
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, ValidationError, validates_schema



# Define ServiceTicket Schema
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True 

    # Include customer details (Nested)
    customer = Nested("CustomerSchema", only=("id", "name", "email", "phone"))

    # Include assigned mechanics (Many-to-Many Relationship)
    service_mechanics = Nested("ServiceMechanicSchema", only=("mechanic_id", "mechanic.name"), many=True)

    service_mechanics_ids = fields.List(fields.Integer(), required=True, load_only=True)

    @validates_schema
    def validate_mechanics(self, data, **kwargs):
        if not isinstance(data.get('service_mechanics_ids'), list):
            raise ValidationError('Invalid input type.', 'service_mechanics_ids')


    def __init__(self, *args, **kwargs):
        from app.blueprints.customers.schemas import CustomerSchema

        self.customer = Nested(CustomerSchema, only=("id", "name", "email", "phone"))

        super().__init__(*args, **kwargs)


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
