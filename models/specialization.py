from db import db

class SpecializationModel(db.Model):
    __tablename__ = "specializations"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    course_items = db.relationship("Course_itemModel", back_populates="specialization",lazy='dynamic')
