from app.extensions import ma
from app.models import ServiceTicket
from marshmallow_sqlalchemy.fields import Nested


# Define ServiceTicket Schema
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True 

    # Include customer details (Nested)
    customer = Nested("CustomerSchema", only=("id", "name", "email", "phone"))

    # Include assigned mechanics (Many-to-Many via ServiceMechanic)
    mechanics = Nested("MechanicSchema", only=("id", "name", "email", "phone"), many=True)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
