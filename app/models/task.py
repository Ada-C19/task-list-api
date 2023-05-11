from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates = "task")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=data_dict.get("completed_at")
        )

    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=not not self.completed_at
        )
