from app import db
from datetime import datetime 
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship



class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    
    goal = db.relationship("Goal", back_populates="tasks")

    def to_result(self):
        is_complete = True
        if not self.completed_at:
            is_complete = False
        task_response = {
            "id":self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete,
        }

        if self.goal_id:
            task_response["goal_id"] = self.goal_id

        return task_response
# def to_dict(self):
#         task_as_dict = {}
#         task_as_dict["id"] = self.id
#         task_as_dict["title"] = self.title
#         task_as_dict["description"] = self.description
#         task_as_dict["completed_at"] = self.completed_at

#         return task_as_dict