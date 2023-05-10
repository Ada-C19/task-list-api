from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    def to_dict_goal(self):
        return {
            "goal": {
            "id": self.goal_id,
            "title": self.title
            }
        }
