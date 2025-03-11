from flask import Flask
from .extensions import db, ma
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.serviceMechanics import service_mechanics_bp
from .blueprints.serviceTickets import service_tickets_bp

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Adding our db extension to our app
    db.init_app(app) 

    # Adding our ma extension to our app
    ma.init_app(app)

    # Registering our blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_mechanics_bp, url_prefix='/service_mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')


    return app