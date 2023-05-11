from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)

    def to_goals_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    @classmethod
    def from_goals_dict(cls, task_data):
        return cls(
            title = task_data["title"]
        )