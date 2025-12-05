from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.course_item import Course_itemModel
from models.specialization import Specialization_model
from schemas import Course_ItemSchema, Course_ItemUpdateSchema, PlainCourse_ItemSchema

blp = Blueprint("course_items", __name__, description="Operations on course items")


def get_or_404_course_item(course_item_id):
    return Course_itemModel.query.get_or_404(course_item_id)

def get_or_404_specialization(specialization_id):
    return Specialization_model.query.get_or_404(specialization_id)

@blp.route("/course_items")
class CourseItemList(MethodView):
    @blp.response(200, PlainCourse_ItemSchema(many=True))
    def get(self):
        return Course_itemModel.query.all()
    
    @jwt_required()
    @blp.arguments(Course_ItemSchema)
    @blp.response(201, PlainCourse_ItemSchema)
    def post(self, course_item_data):
        # Check if course item with same name already exists
        if Course_itemModel.query.filter_by(name=course_item_data["name"]).first():
            abort(400, message="A course item with that name already exists.")
        
        # Check if specialization exists
        specialization = Specialization_model.query.get(course_item_data["specialization_id"])
        if not specialization:
            abort(404, message="Specialization not found.")
        
        # Create new course item
        course_item = Course_itemModel(
            name=course_item_data["name"],
            type=course_item_data["type"],
            specialization_id=course_item_data["specialization_id"]
        )
        
        # Add to database
        db.session.add(course_item)
        db.session.commit()
        
        return course_item

@blp.route("/course_item/<string:course_item_id>")
class CourseItem(MethodView):
    @blp.response(200, PlainCourse_ItemSchema)
    def get(self, course_item_id):
        """Get a specific course item (public)"""
        course_item = get_or_404_course_item(course_item_id)
        return course_item
    
    @jwt_required()
    @blp.arguments(Course_ItemUpdateSchema)
    @blp.response(200, PlainCourse_ItemSchema)
    def put(self, course_item_data, course_item_id):
        """Update a course item (requires authentication)"""
        course_item = get_or_404_course_item(course_item_id)
        
        # Update fields
        if "name" in course_item_data:
            # Check if name already exists (excluding current item)
            if Course_itemModel.query.filter_by(name=course_item_data["name"]).first():
                abort(400, message="A course item with that name already exists.")
            course_item.name = course_item_data["name"]
        
        if "type" in course_item_data:
            course_item.type = course_item_data["type"]
        
        db.session.commit()
        return course_item
    
    @jwt_required()
    def delete(self, course_item_id):
        """Delete a course item (requires authentication)"""
        course_item = get_or_404_course_item(course_item_id)
        db.session.delete(course_item)
        db.session.commit()
        return {"message": "Course item deleted."}

@blp.route("/specialization/<string:specialization_id>/course_items")
class CourseItemsBySpecialization(MethodView):
    @blp.response(200, PlainCourse_ItemSchema(many=True))
    def get(self, specialization_id):
        """Get all course items for a specialization (public)"""
        specialization = get_or_404_specialization(specialization_id)
        return specialization.course_items