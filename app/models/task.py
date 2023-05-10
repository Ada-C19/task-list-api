from app import db
from flask import make_response 

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String)
    description=db.Column(db.String)
    completed_at=db.Column(db.DateTime, nullable=True)
    is_complete= db.Column(db.Boolean, default=False)

    def task_to_dict(self):
        return {
        "task_id": self.task_id,
        "title": self.task_title,
        "description": self.description,
        "is_complete": False if self.completed_at is None else True
        if self.completed_at is not None else None
        }
    @classmethod 
    def create_new_task(cls, request_data):
        if "title" not in request_data or "description" not in request_data:
            raise ValueError("Invalid Request. Missing required fields: title or description")
        is_complete = False if request_data["completed_at"] is None else True
        return cls(
            task_title=request_data["title"].title(),
            description=request_data["description"],
            completed_at=request_data.get("completed_at"),
            is_complete = is_complete
            )