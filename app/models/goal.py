from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        dict = {}
        dict["id"] = self.goal_id
        dict["title"] = self.title
        if self.tasks:
            dict["tasks"] = self.tasks

        return dict

    @classmethod
    def from_dict(self, data):
        return Goal(
            title=data["title"])
