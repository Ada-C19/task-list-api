from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates="task")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
        }
