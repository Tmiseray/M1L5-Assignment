from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import Base, db
import datetime


# Define Customer model
class Customer(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(100), nullable=False)

    # One-to-Many Relationship (Customer -> ServiceTickets)
    service_tickets: Mapped[List['ServiceTicket']] = relationship("ServiceTicket", back_populates="customer", lazy="select")


# Define Mechanic model
class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(100), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    # Many-to-Many Relationship (Mechanic <-> ServiceTickets via ServiceMechanic)
    mechanic_tickets: Mapped[List['ServiceMechanic']] = relationship("ServiceMechanic", back_populates="mechanic", lazy="select")


# Define ServiceTicket model
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)

    # One-to-Many Relationship (ServiceTicket -> Customer)
    customer: Mapped['Customer'] = relationship("Customer", back_populates="service_tickets")
    
    # Many-to-Many Relationship (ServiceTicket <-> Mechanics via ServiceMechanic)
    service_mechanics: Mapped[List['ServiceMechanic']] = relationship("ServiceMechanic", back_populates="service_ticket", lazy="select")


# Define ServiceMechanic model (Join Table)
class ServiceMechanic(Base):  
    __tablename__ = 'service_mechanics'  

    # Composite Primary Key: (service_ticket_id, mechanic_id)
    service_ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'), primary_key=True)

    # Relationships
    service_ticket: Mapped['ServiceTicket'] = relationship("ServiceTicket", back_populates="service_mechanics")
    mechanic: Mapped['Mechanic'] = relationship("Mechanic", back_populates="service_mechanics")

