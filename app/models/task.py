from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True, default = None)

    def to_dict(self):
        return {
            "task_id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "completed_at" : self.completed_at 
        }