import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import Course_itemModel, SpecializationModel
from schemas import Course_ItemSchema, Course_ItemUpdateSchema

blp = Blueprint("Course_Items", __name__, description="Operations on course_items")


@blp.route("/course_item/<string:course_item_id>")
class Course_Item(MethodView):

    @blp.response(200, Course_ItemSchema)
    def get(self, course_item_id):
        course_item = Course_itemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course_Item not found.")
        return course_item

    def delete(self, course_item_id):
        course_item = Course_itemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course_Item not found.")

        db.session.delete(course_item)
        db.session.commit()
        return {"message": "Course_Item deleted."}

    @blp.arguments(Course_ItemUpdateSchema)
    @blp.response(200, Course_ItemSchema)
    def put(self, course_item_data, course_item_id):
        course_item = Course_itemModel.query.get(course_item_id)
        if not course_item:
            abort(404, message="Course_Item not found.")

        # Prevent duplicate (same name + same specialization)
        duplicate = Course_itemModel.query.filter(
            Course_itemModel.name == course_item_data["name"],
            Course_itemModel.specialization_id == course_item_data["specialization_id"],
            Course_itemModel.id != course_item_id
        ).first()

        if duplicate:
            abort(400, message="Course_Item with this name already exists in the specialization.")

        course_item.name = course_item_data["name"]
        course_item.type = course_item_data["type"]
        course_item.specialization_id = course_item_data["specialization_id"]

        db.session.commit()
        return course_item

@blp.route("/course_item")
class Course_ItemList(MethodView):

    @blp.response(200, Course_ItemSchema(many=True))
    def get(self):
        return Course_itemModel.query.all()

    @blp.arguments(Course_ItemSchema)
    @blp.response(201, Course_ItemSchema)
    def post(self, course_item_data):

        # Check duplicate
        existing = Course_itemModel.query.filter_by(
            name=course_item_data["name"],
            specialization_id=course_item_data["specialization_id"]
        ).first()

        if existing:
            abort(400, message="Course_Item already exists.")

        # Create
        new_item = Course_itemModel(
            id=uuid.uuid4().hex,
            name=course_item_data["name"],
            type=course_item_data["type"],
            specialization_id=course_item_data["specialization_id"]
        )

        db.session.add(new_item)
        db.session.commit()

        return new_item
