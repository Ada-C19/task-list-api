from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        return dict(
                id=self.id,
                title=self.title
                )

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(title=goal_data["title"])


