from app import db
from app.models.goal import Goal
from app.route_helpers import validate_model

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column (db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    
    @classmethod
    def from_dict(cls, dict):
        new_task = Task(
            title=dict["title"],
            description=dict["description"],
            completed_at=dict.get("completed_at"),
            goal=validate_model(Goal, dict.get("goal_id")) if dict.get("goal_id") else None
        )
        return new_task
