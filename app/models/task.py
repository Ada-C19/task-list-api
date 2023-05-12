from app import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_dict = dict(
                id=self.id,
                title=self.title,
                description=self.description,
                is_complete=bool(self.completed_at),
            )
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict



    @classmethod
    def from_dict(cls, task_data): 
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"],
        )
        if "completed_at" in task_data:
            completed_at = datetime(task_data["completed_at"])
            new_task.completed_at = completed_at
        return new_task