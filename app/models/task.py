from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)
    goals = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
        title=task_data["title"],
        description=task_data["description"]
    )
        return new_task
    def to_dic(self):
        task_dic = {
            "task": {
                "id": self.task_id,
                "title": self.title,
                "description": self.description, 
                "is_complete": True if self.completed_at else False
            }
        }
        if self.goal_id:
            task_dic["task"]["goal_id"] = self.goal_id
        return task_dic