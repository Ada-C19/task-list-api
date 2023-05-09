from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column (db.String)
    completed_at = db.Column(db.DateTime)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
    
    @classmethod
    def from_dict(cls, dict):
        new_task = Task(
            title=dict["title"],
            description=dict["description"],
            completed_at=dict.get("completed_at")
        )
        return new_task
