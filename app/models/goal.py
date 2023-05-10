from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goals", lazy=True)

    def to_dic(self):
        goal_dic = {
        "goal": {
            "id": self.goal_id,
            "title": self.title
        }
    }
        return goal_dic