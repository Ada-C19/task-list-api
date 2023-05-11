from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates = "tasks")

    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        
    @classmethod
    def from_json(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body.get("completed_at"),
            goal_id=request_body.get("goal_id")
        )


