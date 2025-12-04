from db import db
import uuid  

class Course_itemModel(db.Model):
    __tablename__ = "course_items"
    
    id = db.Column(db.String(80), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    
    specialization_id = db.Column(db.String(80), db.ForeignKey("specializations.id"), nullable=False)
    
    specialization = db.relationship("Specialization_model", back_populates="course_items")
