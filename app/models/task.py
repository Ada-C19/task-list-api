from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(255))
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, task_details):
        new_task = cls(
            title=task_details["title"],
            description=task_details["description"],
            completed_at=task_details.get("completed_at", None)
        )

        return new_task
    
    def is_complete(self):
        if self.completed_at:
            return True
        return False

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete(),
            "goal_id": self.goal_id
        }
    
    # use this function for PATCH method
    def update_fields(self, update_dict):
        self.title = update_dict.get("title", self.title)
        self.description = update_dict.get("description", self.description)
        self.completed_at = update_dict.get("completed_at", self.completed_at)