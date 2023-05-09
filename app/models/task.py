from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if self.goal_id:
            return {
                "id": self.id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
                }
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
            }
    
    def to_dict_complete(self):
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": True
            }