from flask import Flask
from flask_smorest import Api
from resources.course_item import blp as CourseItemBlueprint
from resources.specializations import blp as SpecializationBlueprint
from db import db
import models
import os

def create_app(db_url=None):
    app = Flask(__name__)

    # Flask-Smorest / Swagger configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Specialization REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"                  # Base path for OpenAPI
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False   # recommended

    # Initialize SQLAlchemy
    db.init_app(app)

    # Create tables inside app context (runs once at startup)
    with app.app_context():
        db.create_all()

    # Initialize API
    api = Api(app)

    # Register blueprints
    api.register_blueprint(CourseItemBlueprint)
    api.register_blueprint(SpecializationBlueprint)

    return app
