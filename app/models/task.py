from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        dict = {}
        dict["id"] = self.task_id
        dict["title"] = self.title
        dict["description"] = self.description
        dict["is_complete"] = bool(self.completed_at)
        if self.goal_id:
            dict["goal_id"] = self.goal_id

        return dict

    @classmethod
    def from_dict(self, data):
        return Task(
            title=data["title"],
            description=data["description"])
