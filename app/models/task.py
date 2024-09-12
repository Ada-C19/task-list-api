from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_dict = dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at != None)
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict
    

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                       description=task_data["description"],
                       completed_at=task_data.get("completed_at"))

        return new_task
                




