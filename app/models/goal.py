from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def to_result(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
