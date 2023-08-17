from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task = {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": False,
        }
        if self.completed_at is not None:
            task["is_complete"] = True
        if self.goal_id is not None:
            task["goal_id"] = self.goal_id
        return task
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        return new_task