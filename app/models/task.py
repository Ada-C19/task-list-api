from app import db
from flask import make_response


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'),nullable=True)


    def to_dict(self):
        return dict(
                id=self.id,
                title=self.title,
                description=self.description,
                is_complete=bool(self.completed_at)
            )


    @classmethod
    def from_dict(cls, task_data): 
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"]
        )
        if "completed_at" in task_data:
            new_task.completed_at=task_data["completed_at"]
        return new_task