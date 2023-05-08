from app import db
from sqlalchemy.sql import false

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, server_default=None)
