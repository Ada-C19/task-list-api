from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")


    @classmethod
    def from_dict_goals(cls, goal_data):
        new_goal = Goal(
            title = goal_data["title"]
        )

        return new_goal

    def to_dict_goals(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
