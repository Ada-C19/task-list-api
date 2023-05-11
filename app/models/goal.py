from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    task = db.relationship("Task", back_populates = "goal")

    @classmethod
    def from_dict(cls, data_dict):
        new_goal = Goal(title=data_dict["title"])
        return new_goal

    def to_dict(self):
        return dict(
        id=self.goal_id,
        title=self.title
        )