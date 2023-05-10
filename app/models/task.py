from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if self.completed_at:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": True,
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False,
            }
        
    def to_dict_in_goals(self):
        if self.completed_at:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": True,
                "goal_id": self.goal_id
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False,
                "goal_id": self.goal_id
            }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"],
            description = data_dict["description"],
        )