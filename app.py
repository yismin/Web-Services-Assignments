from flask import Flask
from flask import request
app=Flask(__name__)

specialization=[{"name":"IT",
                 "course_item" :[{"name":"web services",
                                   "Type":"Mandatory"}]}]


@app.get("/specialization")
def get_specializations():
    return {"specializations": specialization}

@app.post("/specialization")
def create_specialization():
    request_data=request.get_json()
    new_specialization={"name":request_data["name"],"course_items":[]}
    specialization.append(new_specialization)
    return new_specialization,201

@app.post("/specialization/<string:name>/course_item")
def create_course_item(name):
    for spec in specialization:
        if spec["name"]==name:
            request_data=request.get_json()
            new_course_item={"name":request_data["name"],"Type":request_data["Type"]}
            spec["course_item"].append(new_course_item)
            return new_course_item,201
        return {"message":"specialization not found"},404

@app.get("/specialization/<string:name>")
def get_specialization(name):
    for spec in specialization:
        if spec["name"]==name:
            return spec
    return {"message":"specialization not found"},404

@app.get("/specialization/<string:name>/course_item")
def get_course_item_in_specialization(name):
    for spec in specialization:
        if spec["name"]==name:
            return {"course_items":spec["course_item"]}
    return {"message":"specialization not found"},404