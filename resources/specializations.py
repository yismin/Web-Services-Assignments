from flask import request, abort
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import Blueprint
from schemas import Specializations_Schema
from db import db
from models import SpecializationModel   

blp = Blueprint("Specializations", __name__, description="Operations on specializations")

@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):

    @blp.response(200, Specializations_Schema)
    def get(self, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, description="Specialization not found")
        return specialization

    def delete(self, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, description="Specialization not found")

        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Specialization deleted"}

    def put(self, specialization_id):
        specialization = SpecializationModel.query.get(specialization_id)
        if not specialization:
            abort(404, description="Specialization not found")

        data = request.get_json()
        if not data or "name" not in data:
            abort(400, description="Bad request. 'name' is required")

        # Prevent duplicate names
        duplicate = SpecializationModel.query.filter(
            SpecializationModel.name == data["name"],
            SpecializationModel.id != specialization_id
        ).first()

        if duplicate:
            abort(400, description="Specialization name already exists")

        specialization.name = data["name"]
        db.session.commit()

        return specialization


@blp.route("/specialization")
class SpecializationList(MethodView):

    @blp.response(200, Specializations_Schema(many=True))
    def get(self):
        return SpecializationModel.query.all()

    @blp.arguments(Specializations_Schema)
    @blp.response(201, Specializations_Schema)
    def post(self, specializations_data):

        # Check duplicates
        existing = SpecializationModel.query.filter_by(
            name=specializations_data["name"]
        ).first()

        if existing:
            abort(400, description="Specialization already exists")

        # Create
        specialization = SpecializationModel(
            id=uuid4().hex,
            name=specializations_data["name"]
        )

        db.session.add(specialization)
        db.session.commit()

        return specialization
