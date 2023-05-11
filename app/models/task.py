from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    completed_at = db.Column(db.DateTime, nullable = True, default = None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable = True)
    goal = db.relationship("Goal", back_populates = "tasks")

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(
            title = task_data.get("title"),
            description = task_data.get("description"),
            completed_at = task_data.get("completed_at")
        )
        return new_task

    def to_dict(self):
        tasks_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal_id:
            tasks_dict["goal_id"] = self.goal_id
        return tasks_dict
    
    def as_task_dict(self):
        task_dict = { "task": self.to_dict()}
        return task_dict
    
    def mark_as_completed(self):
        self.completed_at = datetime.utcnow()

    
        