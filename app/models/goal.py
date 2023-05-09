from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)


def to_dict(self):
    goal_as_dict = {
        "id": self.goal_id,
        "title": self.title,
    }

    return goal_as_dict


@classmethod
def from_dict(cls, goal_data):
    new_goal = Goal(title=goal_data["title"])
    return new_goal
