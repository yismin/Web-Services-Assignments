from marshmallow import Schema, fields

class specializationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()

class PlainCourse_ItemSchema(Schema):
    course_item_id =fields.Str(dump_only=True)
    name= fields.Str(required=True)
    type= fields.Str(required=True)
    #specialization_id= fields.Str(required=True)

class Course_ItemUpdateSchema(Schema):
    name= fields.Str(required=True)
    type= fields.Str(required=True)

class PlainSpecializations_Schema(Schema):
    specialization_id =fields.Str(dump_only=True)
    name= fields.Str(required=True)

class Course_ItemSchema(PlainCourse_ItemSchema):
    specialization_id= fields.Int(required=True,load_only=True)
    specialization= fields.Nested(PlainSpecializations_Schema(), dump_only=True)

class Specializations_Schema(PlainSpecializations_Schema):
    specialization_id =fields.Str(dump_only=True)
    course_items= fields.List(fields.Nested( PlainCourse_ItemSchema(),dump_only=True))