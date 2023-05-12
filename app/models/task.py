from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)

    def to_dict(self):
        
        if self.goal_id == None:
            return {"task": {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": False
                }}
        elif self.goal_id >= 1:
            return {
                "task": {
                    "id": self.id,
                    "goal_id": self.goal_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": False
                }}
