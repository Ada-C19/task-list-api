from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    completed_at = db.Column(db.DateTime, default=None)

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    
    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
        }

    @classmethod
    def from_dict(cls,task_details):
        new_task = Task(title=task_details["title"], description=task_details["description"] )
        return new_task