from flask import Flask, request
import uuid
from db import specializations, course_items
from flask_smorest import abort

app = Flask(__name__)

#specializations=[{"name": "IT", "course_items":[{"name":"Web Services", "Type":"Mandatory"}]}]

#OK#
@app.get("/specialization")
def get_specializations():
    return{"specialization":list(specializations.values())}

#OK#
@app.post("/specialization")
def create_specializations():
    specialization_data=request.get_json()
    if "name" not in specialization_data:
        abort(400, message="Bad Request. Ensure 'name' is included in the JSON payload")

    for specialization in specializations.values():
        if(specialization_data["name"]==specialization["name"]) and (specialization_data["specialization_id"]==specialization["specialization_id"]):
            abort(400, message="specialization already exists")

    specialization_id=uuid.uuid4().hex
    specialization={**specialization_data, "id": specialization_id}
    specializations[specialization_id]=specialization
    return specialization, 201




@app.post("/course_item")
def create_course_item():
    course_item_data=request.get_json()
    if (
        "type" not in course_item_data
        or "specialization_id" not in course_item_data
        or "name" not in course_item_data
    ):
        abort(400, message="Bad request. Ensure 'type', 'specialization_id', and 'name' are included in the JSON paylaod")
   
    for course_item in course_items.values():
        if(course_item_data["name"]==course_item["name"]) and (course_item_data["specialization_id"]==course_item["specialization_id"]):
            abort(400, message="Course Item already exists")
   
    course_item_id=uuid.uuid4().hex
   
    course_item={**course_item_data, "id": course_item_id}
    course_items[course_item_id]=course_item
    return course_item, 201
   
   
           
   

#@app.get("/specialization/<string:name>")
#def get_specialization(name):
#    for specialization in specializations:
#        if specialization["name"]==name:
#            return specialization
#        return{"message":"Specialization not found"}, 404

#ok
@app.get("/specialization/<string:specialization_id>")
def get_specialization(specialization_id):
    try:
        return specializations[specialization_id]
    except KeyError:
        #return {"message": "Scpecialization not found"}, 404
        abort(404, message="Scpecialization not found")



#@app.get("/specialization/<string:name>/course_item")
#def get_course_item_in_specialization(name):
#    for specialization in specializations:
#        if specialization["name"]==name:
#            return {"course_items": specialization["course_items"]}
#        return{"message":"Specialization not found"}, 404


@app.get("/course_item/<string:course_item_id>")
def get_course_item(course_item_id):
    try:
        return course_items[course_item_id]
    except KeyError:
        #return {"message": "Course Item not found"}, 404
        abort(404, message= "Course Item not found")

@app.delete("/specialization/<string:specialization_id>")
def delete_specialization(specialization_id):
    try:
        del specializations[specialization_id]
        return {"message": "Specialization deleted"}
    except KeyError:
        abort(404, message="Specialization not found")

@app.put("/course_item/<string:course_item_id>")
def update_course_item(course_item_id):
    course_item_data=request.get_json()
    if ("type" not in course_item_data or "specialization_id" not in course_item_data or "name" not in course_item_data):
        abort(400, message="Bad request. Ensure 'type', 'specialization_id', and 'name' are included in the JSON paylaod")
    try:
        course_item=course_items[course_item_id]
        course_item|course_item_data
        return course_item
    except KeyError:
        abort(404, message="Course Item not found")