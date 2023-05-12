from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }
    
    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" not in task_data:
            task_data["completed_at"] = None
        
        return Task(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"]
        )