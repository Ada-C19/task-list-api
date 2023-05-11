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
        if not self.completed_at:
            return {
                "task": {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": False
                }
            }
        else:
            return {
                "task": {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": True
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
