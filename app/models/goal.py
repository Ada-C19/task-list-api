from app import db

#var si hereda de task
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }

    @classmethod
    def from_dict(cls, goal_data):
        new_task = Goal(title=goal_data["title"])
        return new_task
