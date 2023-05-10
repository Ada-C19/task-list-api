from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)

    def to_dict(self):
        goal_dict = {}
        goal_dict["id"] == self.goal_id
        goal_dict["title"] == self.title
        return goal_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"]
        )