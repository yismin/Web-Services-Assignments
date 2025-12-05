from marshmallow import Schema, fields

class PlainCourse_ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)

class Course_ItemUpdateSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)
   
class PlainSpecialization_Schema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class SpecializationUpdateSchema(Schema):
    name = fields.Str(required=True)  

class Course_ItemSchema(PlainCourse_ItemSchema):
    specialization_id = fields.Str(required=True, load_only=True)
    specialization = fields.Nested(PlainSpecialization_Schema, dump_only=True)

class Specialization_Schema(PlainSpecialization_Schema):
    course_items = fields.Nested(PlainCourse_ItemSchema, many=True, dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  # Never return password in response