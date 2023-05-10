from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if not self.goal_id: 
            return {
                "id":self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at is not None
            }
        
        return {
                "id":self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at is not None,
                "goal_id" : self.goal_id
            }