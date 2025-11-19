import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import course_items

blp = Blueprint("Course_Items", __name__, description="Operations on course_items")


@blp.route("/course_item/<string:course_item_id>")
class Course_Item(MethodView):
    def get(self, course_item_id):
        try:
            return course_items[course_item_id]
        except KeyError:
            abort(404, message="Course_Item not found.")

    def delete(self, course_item_id):
        try:
            del course_items[course_item_id]
            return {"message": "Course_item deleted."}
        except KeyError:
            abort(404, message="Course_Item not found.")

    def put(self, course_item_id):
        course_item_data = request.get_json()
        if "type" not in course_item_data or "name" not in course_item_data:
            abort(
                400,
                message="Bad request. Ensure 'type', and 'name' are included in the JSON payload.",
            )
        try:
            course_item = course_items[course_item_id]
            course_item |= course_item_data

            return course_item
        except KeyError:
            abort(404, message="Course_Item not found.")


@blp.route("/course_item")
class ItemList(MethodView):
    def get(self):
        return {"course_items": list(course_items.values())}

    def post(self):
        course_item_data = request.get_json()
        if (
            "type" not in course_item_data
            or "specialization_id" not in course_item_data
            or "name" not in course_item_data
        ):
            abort(
                400,
                message="Bad request. Ensure 'type', 'specialization_id', and 'name' are included in the JSON payload.",
            )
        for course_item in course_items.values():
            if (
                course_item_data["name"] == course_items["name"]
                and course_item_data["specialization_id"] == course_items["specialization_id"]
            ):
                abort(400, message="Course_Item already exists.")

        course_item_id = uuid.uuid4().hex
        course_item = {**course_item_data, "id": course_item_id}
        course_items[course_item_id] = course_item

        return course_item