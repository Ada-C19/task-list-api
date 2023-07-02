from app import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "task": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
            }
        }

        if self.goal_id:
            task_dict["task"]["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def from_dict(cls, task_dict):
        try:
            return cls(title=task_dict["title"],
                       description=task_dict["description"],
                       completed_at=task_dict.get("completed_at", None))
        except KeyError as error:
            return f"Missing key {error}"
