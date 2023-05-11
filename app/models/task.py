from app import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.Date, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if self.goal_id:
            return {
                "task": {
                    "id": self.id,
                    "goal_id": self.goal_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": bool(self.completed_at)
                }
            }
        else:
            return {
                "task": {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": bool(self.completed_at)
                }
            }

     
    @classmethod
    def from_dict(cls, task_dict):
        try:
            if not task_dict.get("completed_at"):
                return cls(title=task_dict["title"],
                           description=task_dict["description"],
                           completed_at=None)
            else:
                return cls(title=task_dict["title"],
                           description=task_dict["description"],
                           completed_at=task_dict["completed_at"])
        except KeyError as error:
            return f"Missing or invalid key {error}"
