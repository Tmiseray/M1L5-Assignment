from app.extensions import ma
from app.models import ServiceMechanic
from marshmallow_sqlalchemy.fields import Nested


# Define ServiceMechanic Schema
class ServiceMechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceMechanic
        include_fk = True

    # Optionally include mechanic and service ticket details (Nested)
    mechanic = Nested("MechanicSchema", only=("id", "name"))
    service_ticket = Nested("ServiceTicketSchema", only=("id", 
                                                         "VIN", 
                                                         "service_date", 
                                                         "service_desc"))

    def __init__(self, *args, **kwargs):
        from app.blueprints.mechanics.schemas import MechanicSchema
        from app.blueprints.serviceTickets.schemas import ServiceTicketSchema

        self.mechanic = Nested(MechanicSchema, only=("id", "name"))
        self.service_ticket = Nested(ServiceTicketSchema, only=("id", 
                                                                "VIN", 
                                                                "service_date", 
                                                                "service_desc"))

        super().__init__(*args, **kwargs)


service_mechanic_schema = ServiceMechanicSchema()
service_mechanics_schema = ServiceMechanicSchema(many=True)
