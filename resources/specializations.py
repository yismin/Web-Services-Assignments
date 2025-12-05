import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.specialization import Specialization_model
from schemas import Specialization_Schema, PlainSpecialization_Schema, SpecializationUpdateSchema

blp = Blueprint("specializations", __name__, description="Operations on specializations")

# Helper functions
def check_specialization_exists(name, exclude_id=None):
    """Check if a specialization with the given name already exists."""
    query = Specialization_model.query.filter_by(name=name)
    if exclude_id:
        query = query.filter(Specialization_model.id != exclude_id)
    return query.first() is not None

def get_or_404_specialization(specialization_id):
    """Get specialization or return 404 if not found."""
    return Specialization_model.query.get_or_404(specialization_id)

def validate_specialization_data(specialization_data, exclude_id=None):
    """Validate specialization data (check for duplicates)."""
    if "name" in specialization_data:
        if check_specialization_exists(specialization_data["name"], exclude_id):
            abort(400, message="A specialization with that name already exists.")

def create_specialization(specialization_data):
    """Create a new specialization."""
    validate_specialization_data(specialization_data)
    
    specialization = Specialization_model(name=specialization_data["name"])
    db.session.add(specialization)
    db.session.commit()
    return specialization

def update_specialization(specialization, specialization_data):
    """Update an existing specialization."""
    validate_specialization_data(specialization_data, exclude_id=specialization.id)
    
    if "name" in specialization_data:
        specialization.name = specialization_data["name"]
    
    db.session.commit()
    return specialization

# Routes
@blp.route("/specializations")
class SpecializationList(MethodView):
    @blp.response(200, PlainSpecialization_Schema(many=True))
    def get(self):
        """Get all specializations (public)"""
        return Specialization_model.query.all()
    
    @jwt_required()
    @blp.arguments(Specialization_Schema)
    @blp.response(201, PlainSpecialization_Schema)
    def post(self, specialization_data):
        """Create a new specialization (requires authentication)"""
        return create_specialization(specialization_data)

@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):
    @blp.response(200, PlainSpecialization_Schema)
    def get(self, specialization_id):
        """Get a specific specialization (public)"""
        specialization = get_or_404_specialization(specialization_id)
        return specialization
    
    @jwt_required()
    @blp.arguments(SpecializationUpdateSchema)
    @blp.response(200, PlainSpecialization_Schema)
    def put(self, specialization_data, specialization_id):
        """Update a specialization (requires authentication)"""
        specialization = get_or_404_specialization(specialization_id)
        return update_specialization(specialization, specialization_data)
    
    @jwt_required()
    def delete(self, specialization_id):
        """Delete a specialization (requires authentication)"""
        specialization = get_or_404_specialization(specialization_id)
        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Specialization deleted."}