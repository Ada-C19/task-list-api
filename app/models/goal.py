from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    # FROM_DICT (request)
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title=goal_data["title"]
        )

    # goal TO_DICT (response should be a dict that is the value of key "goal" in a dict)
    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title

        return goal_as_dict