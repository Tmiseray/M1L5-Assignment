
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow


# Create a base class for our models
class Base(DeclarativeBase):
    pass

# Instantiate your SQLAlchemy database
db = SQLAlchemy(model_class = Base)

# Instantiate your Marshmallow object
ma = Marshmallow()