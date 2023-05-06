from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
    
    @classmethod
    def from_dict(cls, goal_dict):
        return Goal(
            title=goal_dict["title"]
        )