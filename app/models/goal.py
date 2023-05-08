from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks= db.relationship("Task", back_populates="goal")

    def to_dict(self):
        as_a_dict = {}
        as_a_dict["id"] = self.goal_id
        as_a_dict["title"] = self.title

        return as_a_dict