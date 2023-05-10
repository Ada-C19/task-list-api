from app import db

# One goal has many tasks
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    tasks = db.relationship('Task', back_populates="goal")

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }