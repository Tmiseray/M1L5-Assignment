from app.extensions import ma
from app.models import ServiceMechanic
from marshmallow_sqlalchemy.fields import Nested


# Define ServiceMechanic Schema
class ServiceMechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceMechanic
        include_fk = True 

    # Optionally include mechanic and service ticket details (Nested)
    mechanic = Nested("MechanicSchema", only=("id", "name", "email", "phone"))
    service_ticket = Nested("ServiceTicketSchema", only=("id", "VIN", "service_date", "service_desc"))

service_mechanic_schema = ServiceMechanicSchema()
service_mechanics_schema = ServiceMechanicSchema(many=True)
