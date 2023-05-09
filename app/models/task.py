from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    # goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))
    # goal = db.relationship("Goal", back_populates = "tasks")

    @classmethod
    def from_dict(cls, task_data):
        task = Task(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = None
        )

        return task
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
        }