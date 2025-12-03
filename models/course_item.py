from db import db

class Course_itemModel(db.Model):
    __tablename__ = "course_items"
    id = db.Column(db.String,primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type= db.Column(db.String(80),nullable=False)
    specialization_id= db.Column(db.Integer, db.ForeignKey("specializations.id") ,unique=False, nullable=False)
    specialization=db.relationship("SpecializationModel",back_populates='course_items')