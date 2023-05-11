from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String, default=None)
    completed_at = db.Column(db.DateTime, default=None)
     #one to many relationship syntax
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        is_complete = True if self.completed_at else False

        task_dict = {
            "task": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
            }
        }

        if self.goal_id is not None:
            task_dict["task"]["goal_id"]= self.goal_id
        
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data["completed_at"]
        )