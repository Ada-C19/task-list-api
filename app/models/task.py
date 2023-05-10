from app import db
from flask import make_response 

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String)
    task_description=db.Column(db.String)
    completed_at=db.Column(db.DateTime, nullable=True)

    def task_to_dict(self):
        return {
        "task_id": self.task_id,
        "task_title": self.task_title,
        "task_description": self.task_description,
        "completed_at": self.completed_at.strftime("%Y-%m-%d %H:%M:%S")
        if self.completed_at is not None else None
        }
    @classmethod 
    def create_new_task(cls, request_data):
        if "task_title" not in request_data or "task_description" not in request_data:
            raise ValueError("Invalid Request. Missing required fields: name or description")
        return cls(
            task_title=request_data["task_title"].title(),
            task_description=request_data["task_description"],
            completed_at=request_data.get("completed_at")
        )