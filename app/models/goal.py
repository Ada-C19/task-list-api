from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
                "goal": {
                    "id": self.id,
                    "title": self.title,
                }
            }

    @classmethod
    def from_dict(cls, goal_dict):
        try:
            return cls(
                title=goal_dict["title"]
            )
        except KeyError as error:
            return f"Missing or invalid key {error}"

