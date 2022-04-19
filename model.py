from app import db
from sqlalchemy.orm import relationship

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    date = db.Column(db.Date, unique=False, nullable=True)
    completed = db.Column(db.Boolean, unique=False, nullable=True, default=False)

# db.create_all()