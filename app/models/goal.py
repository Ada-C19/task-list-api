from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def to_dict(self):
        dict = {}
        dict["id"] = self.goal_id
        dict["title"] = self.title
        return dict

    @classmethod
    def from_dict(self, data):
        return Goal(
            title=data["title"])
