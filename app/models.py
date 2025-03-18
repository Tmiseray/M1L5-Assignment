from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import date


# Create a base class for our models
class Base(DeclarativeBase):
    pass

# Instantiate your SQLAlchemy database
db = SQLAlchemy(model_class = Base)


# Define Customer model
class Customer(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(100), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    # One-to-Many Relationship (Customer -> ServiceTickets)
    service_tickets: Mapped[Optional[List['ServiceTicket']]] = db.relationship("ServiceTicket", back_populates="customer", lazy="select")


# Define Mechanic model
class Mechanic(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(100), nullable=False)
    role: Mapped[str] = mapped_column(db.String(100), nullable=False, default="Mechanic")
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    # Many-to-Many Relationship (Mechanic <-> ServiceTickets via ServiceMechanic)
    mechanic_tickets: Mapped[Optional[List['ServiceMechanic']]] = db.relationship("ServiceMechanic", back_populates="mechanic", lazy="select")


# Define ServiceTicket model
class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)

    # One-to-Many Relationship (ServiceTicket -> Customer)
    customer: Mapped[Optional['Customer']] = db.relationship("Customer", back_populates="service_tickets")
    
    # Many-to-Many Relationship (ServiceTicket <-> Mechanics via ServiceMechanic)
    service_mechanics: Mapped[List['ServiceMechanic']] = db.relationship("ServiceMechanic", back_populates="service_ticket", lazy="select", cascade="all, delete-orphan")


# Define ServiceMechanic model (Join Table)
class ServiceMechanic(Base):  
    __tablename__ = 'service_mechanics'  

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'))
    mechanic_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey('mechanics.id', ondelete='SET NULL'), nullable=True)
    start_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(db.Date, nullable=True)

    # Relationships
    service_ticket: Mapped['ServiceTicket'] = db.relationship("ServiceTicket", back_populates="service_mechanics")
    mechanic: Mapped[Optional['Mechanic']] = db.relationship("Mechanic", back_populates="mechanic_tickets")


# Define Inventory model
'''
id: Mapped[int] = mapped_column(primary_key=True)
name: Mapped[str] = mapped_column(db.String(100), nullable=False)
price: Mapped[float] = mapped_column(db.Float, nullable=False)
stock: Mapped[int] = mapped_column(db.Integer, nullable=False)
'''

# Define ServiceItems model
'''
item: Inventory
quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
'''

# Define Invoice model
'''
id: Mapped[int] = mapped_column(primary_key=True)
date: Mapped[date] = mapped_column(db.Date, nullable=False, default=date.today())
customer: Customer
mechanic: ServiceMechanic
service_ticket: ServiceTicket
service_items: List[ServiceItems]
total: Mapped[float] = mapped_column(db.Float, nullable=False)
'''