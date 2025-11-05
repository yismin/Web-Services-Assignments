"""from flask import Flask, request, jsonify         
from flask_sqlalchemy import SQLAlchemy           
from dotenv import load_dotenv                       
import os

load_dotenv() 

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Specialization(db.Model):
    __tablename__ = "specialization"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    course_items = db.relationship(
        "CourseItem",
        backref="specialization",
        cascade="all, delete-orphan",
        lazy=True
    )

class CourseItem(db.Model):
    __tablename__ = "course_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    specialization_id = db.Column(db.Integer, db.ForeignKey("specialization.id"), nullable=False)


def specialization_to_dict(s: Specialization):
    return {
        "id": s.id,
        "name": s.name,
        "course_items": [
            {"id": c.id, "name": c.name, "Type": c.type} for c in s.course_items
        ]
    }

@app.get("/specialization")
def get_specializations():
    specs = Specialization.query.all()
    return jsonify([specialization_to_dict(s) for s in specs])

@app.post("/specialization")
def create_specialization():
    data = request.get_json() or {}
    if "name" not in data:
        return jsonify({"message": "name is required"}), 400

    if Specialization.query.filter_by(name=data["name"]).first():
        return jsonify({"message": "specialization already exists"}), 409

    spec = Specialization(name=data["name"])
    db.session.add(spec)
    db.session.commit()
    return jsonify(specialization_to_dict(spec)), 201

@app.get("/specialization/<string:name>")
def get_specialization(name):
    spec = Specialization.query.filter_by(name=name).first()
    if not spec:
        return jsonify({"message": "specialization not found"}), 404
    return jsonify(specialization_to_dict(spec))

@app.post("/specialization/<string:name>/course_item")
def create_course_item(name):
    spec = Specialization.query.filter_by(name=name).first()
    if not spec:
        return jsonify({"message": "specialization not found"}), 404

    data = request.get_json() or {}
    if "name" not in data or "Type" not in data:
        return jsonify({"message": "name and Type are required"}), 400

    course = CourseItem(name=data["name"], type=data["Type"], specialization=spec)
    db.session.add(course)
    db.session.commit()
    return jsonify({"id": course.id, "name": course.name, "Type": course.type}), 201

@app.get("/specialization/<string:name>/course_item")
def get_course_items(name):
    spec = Specialization.query.filter_by(name=name).first()
    if not spec:
        return jsonify({"message": "specialization not found"}), 404
    items = [{"id": c.id, "name": c.name, "Type": c.type} for c in spec.course_items]
    return jsonify(items)

@app.put("/specialization/<string:name>")
def update_specialization(name):
    spec = Specialization.query.filter_by(name=name).first()
    if not spec:
        return jsonify({"message": "specialization not found"}), 404

    data = request.get_json() or {}
    new_name = data.get("name")
    if not new_name:
        return jsonify({"message": "name is required"}), 400

    if Specialization.query.filter_by(name=new_name).first():
        return jsonify({"message": "a specialization with that name already exists"}), 409

    spec.name = new_name
    db.session.commit()
    return jsonify({"message": "specialization updated"})

@app.delete("/specialization/<string:name>")
def delete_specialization(name):
    spec = Specialization.query.filter_by(name=name).first()
    if not spec:
        return jsonify({"message": "specialization not found"}), 404
    db.session.delete(spec)
    db.session.commit()
    return jsonify({"message": f"specialization '{name}' deleted"})

@app.put("/specialization/<string:name>/course_item/<int:course_id>")
def update_course_item(name, course_id):
    spec = Specialization.query.filter_by(name=name).first()
    if not spec:
        return jsonify({"message": "specialization not found"}), 404

    course = CourseItem.query.filter_by(id=course_id, specialization_id=spec.id).first()
    if not course:
        return jsonify({"message": "course_item not found"}), 404

    data = request.get_json() or {}
    course.name = data.get("name", course.name)
    course.type = data.get("Type", course.type)
    db.session.commit()
    return jsonify({"message": "course_item updated"})

@app.delete("/specialization/<string:name>/course_item/<int:course_id>")
def delete_course_item(name, course_id):
    spec = Specialization.query.filter_by(name=name).first()
    if not spec:
        return jsonify({"message": "specialization not found"}), 404

    course = CourseItem.query.filter_by(id=course_id, specialization_id=spec.id).first()
    if not course:
        return jsonify({"message": "course_item not found"}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "course_item deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)"""
