from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def to_dict(self):
        task_dict = {}
        task_dict["id"] = self.task_id
        task_dict["title"] = self.title
        task_dict["description"] = self.description
        task_dict["is_complete"] = self.completed_at != None

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            completed_at=task_dict.get("completed_at")
        )