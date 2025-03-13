from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.serviceTickets import service_tickets_bp


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Adding our db extension to our app
    db.init_app(app) 

    # Adding our ma extension to our app
    ma.init_app(app)

    # Adding our limiter extension to our app
    limiter.init_app(app)


    # Registering our blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')

    # Adding default limit for all routes
    # This ensures that all routes are limited by default
    limiter.limit("30 per hour")(app)


    return app