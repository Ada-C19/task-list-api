from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False    
        return {
            "id" : self.task_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : is_complete
        }
    
    def to_dict_with_goal(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False    
        return {
            "id" : self.task_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : is_complete,
            "goal_id": self.goal_id
        }