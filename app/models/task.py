from app import db
from datetime import datetime

from flask import abort, make_response

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String, nullable=False)
    description= db.Column(db.String, nullable=False)
    completed_at= db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates= "tasks")
    goal_id= db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def to_dict(self):
        as_a_dict = {}
        as_a_dict["id"] = self.task_id
        as_a_dict["title"] = self.title
        as_a_dict["description"] = self.description       
        as_a_dict["is_complete"] = False if self.completed_at is None else True
        if self.goal:
            as_a_dict["goal_id"] = self.goal.goal_id 

        return as_a_dict
    
