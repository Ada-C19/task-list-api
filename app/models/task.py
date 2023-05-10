from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
        
    # Class method to format responses
    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete_status(self.completed_at)
        }
        
    # Class method to return is_complete status dependent on completed_at data
    def is_complete_status(self, completed_at):
        if completed_at is None:
            return False
        else:
            return True
        
    
