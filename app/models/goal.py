from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
    
    @classmethod
    def from_dict(cls, task_data):
        return Goal(
            title=task_data["title"]
        )

