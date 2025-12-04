import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.specialization import Specialization_model
from schemas import Specialization_Schema, PlainSpecialization_Schema, SpecializationUpdateSchema  # We'll need an update schema

blp = Blueprint("specializations", __name__, description="Operations on specializations")

@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):
    @blp.response(200, PlainSpecialization_Schema)
    def get(self, specialization_id):
        specialization = Specialization_model.query.get_or_404(specialization_id)
        return specialization
    
    @blp.arguments(SpecializationUpdateSchema)  # Add this decorator
    @blp.response(200, PlainSpecialization_Schema)
    def put(self, specialization_data, specialization_id):  # Add this method
        specialization = Specialization_model.query.get_or_404(specialization_id)
        
        # Check if name is being updated and if it already exists (excluding current)
        if "name" in specialization_data:
            existing = Specialization_model.query.filter(
                Specialization_model.name == specialization_data["name"],
                Specialization_model.id != specialization_id
            ).first()
            if existing:
                abort(400, message="A specialization with that name already exists.")
            specialization.name = specialization_data["name"]
        
        db.session.commit()
        return specialization
    
    def delete(self, specialization_id):
        specialization = Specialization_model.query.get_or_404(specialization_id)
        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Specialization deleted."}


@blp.route("/specialization")
class SpecializationList(MethodView):
    @blp.response(200, PlainSpecialization_Schema(many=True))
    def get(self):
        return Specialization_model.query.all()
    
    @blp.arguments(Specialization_Schema)
    @blp.response(201, PlainSpecialization_Schema)
    def post(self, specialization_data):
        # Check if specialization with same name already exists
        if Specialization_model.query.filter_by(name=specialization_data["name"]).first():
            abort(400, message="Specialization already exists.")
        
        # Create new specialization
        specialization = Specialization_model(name=specialization_data["name"])
        
        # Add to database
        db.session.add(specialization)
        db.session.commit()
        
        return specialization