from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at
        }
    
    def validate_complete(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
    
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
            }
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"],
            description = data_dict["description"]
        )


