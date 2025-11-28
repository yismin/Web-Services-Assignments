from flask import Flask, request, abort
from uuid import uuid4
from flask.views import MethodView
from db import specializations
from flask_smorest import Blueprint
from schemas import Specializations_Schema

blp = Blueprint("Specializations", __name__, description="Operations on specializations")

@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):
    @blp.response(200, Specializations_Schema)
    def get(self, specialization_id):
        try:
            return specializations[specialization_id]
        except KeyError:
            abort(404, description="Specialization not found")

    def delete(self, specialization_id):
        try:
            del specializations[specialization_id]
            return {"message": "Specialization deleted"}
        except KeyError:
            abort(404, description="Specialization not found")

    def put(self, specialization_id):
        if specialization_id not in specializations:
            abort(404, description="Specialization not found")
        
        data = request.get_json()
        if not data or "name" not in data:
            abort(400, description="Bad request. 'name' is required")
        
        # Prevent duplicate names
        for sp_id, sp in specializations.items():
            if sp["name"] == data["name"] and sp_id != specialization_id:
                abort(400, description="Specialization name already exists")
        
        specializations[specialization_id]["name"] = data["name"]
        return specializations[specialization_id]

@blp.route("/specialization")
class SpecializationList(MethodView):
    @blp.response(200, Specializations_Schema(many=True))
    def get(self):
        return {"specializations": list(specializations.values())}
    
    @blp.arguments(Specializations_Schema)
    @blp.response(201, Specializations_Schema)
    def post(self,specializations_data):
        specialization_data = request.get_json()
        """if "name" not in specialization_data:
            abort(400, description="Bad request. Ensure 'name' is included")
        
       """ # Prevent duplicates
        for specialization in specializations.values():
            if specialization_data["name"] == specialization["name"]:
                abort(400, description="Specialization already exists")

        specialization_id = uuid4().hex
        specialization = {**specialization_data, "id": specialization_id}
        specializations[specialization_id] = specialization
        return specialization, 201
