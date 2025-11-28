from marshmallow import Schema, fields

class specializationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()

class Course_ItemSchema(Schema):
    course_item_id =fields.Str(dump_only=True)
    name= fields.Str(required=True)
    type= fields.Str(required=True)
    specialization_id= fields.Str(required=True)

class Course_ItemUpdateSchema(Schema):
    name= fields.Str(required=True)
    type= fields.Str(required=True)

class Specializations_Schema(Schema):
    specialization_id =fields.Str(dump_only=True)
    name= fields.Str(required=True)
    
