from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self, tasks=False):
        goal_as_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        if tasks:
            goal_as_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(
            title=goal_data["title"],
        )