from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.course_item import Course_itemModel
from models.specialization import Specialization_model
from schemas import Course_ItemSchema, Course_ItemUpdateSchema, PlainCourse_ItemSchema

blp = Blueprint("course_items", __name__, description="Operations on course items")

@blp.route("/course_item/<string:course_item_id>")
class CourseItem(MethodView):
    @blp.response(200, PlainCourse_ItemSchema)
    def get(self, course_item_id):
        course_item = Course_itemModel.query.get_or_404(course_item_id)
        return course_item
    
    @blp.arguments(Course_ItemUpdateSchema)
    @blp.response(200, PlainCourse_ItemSchema)
    def put(self, course_item_data, course_item_id):
        course_item = Course_itemModel.query.get_or_404(course_item_id)
        
        # Update fields
        if "name" in course_item_data:
            # Check if name already exists (excluding current item)
            if Course_itemModel.query.filter(
                Course_itemModel.name == course_item_data["name"],
                Course_itemModel.id != course_item_id
            ).first():
                abort(400, message="A course item with that name already exists.")
            course_item.name = course_item_data["name"]
        
        if "type" in course_item_data:
            course_item.type = course_item_data["type"]
        
        db.session.commit()
        return course_item
    
    def delete(self, course_item_id):
        course_item = Course_itemModel.query.get_or_404(course_item_id)
        db.session.delete(course_item)
        db.session.commit()
        return {"message": "Course item deleted."}


@blp.route("/course_item")
class CourseItemList(MethodView):
    @blp.response(200, PlainCourse_ItemSchema(many=True))
    def get(self):
        return Course_itemModel.query.all()
    
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


# Optional: Get course items by specialization
@blp.route("/specialization/<string:specialization_id>/course_items")
class CourseItemsBySpecialization(MethodView):
    @blp.response(200, PlainCourse_ItemSchema(many=True))
    def get(self, specialization_id):
        specialization = Specialization_model.query.get_or_404(specialization_id)
        return specialization.course_items.all()  # Using .all() because relationship is "dynamic"