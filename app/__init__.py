# app/__init__.py
from flask import Flask
from flask_cors import cross_origin
from .config import Config
from .extensions import db, migrate, jwt, cors, limiter, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, 
                  origins=["http://localhost:3000", "http://localhost:5173"],
                  methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                  allow_headers=["Content-Type", "Authorization"])
    limiter.init_app(app)
    mail.init_app(app)

    # Import models (important for migrations)
    from app.models import User, Category, Product, RefreshToken


    # Register blueprints
    register_blueprints(app)

    # Register CLI commands
    register_commands(app)

    return app


def register_blueprints(app):
    """Register all blueprints"""
    from .blueprints.v1 import auth, products, categories
    app.register_blueprint(auth.bp, url_prefix="/api/v1/auth")
    app.register_blueprint(products.bp, url_prefix="/api/v1/products")
    app.register_blueprint(categories.bp, url_prefix="/api/v1/categories")


def register_commands(app):
    """Register CLI commands"""
    from .seed import init_db, seed_data
    
    app.cli.add_command(init_db)
    app.cli.add_command(seed_data)