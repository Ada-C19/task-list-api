from app import db

# create Task class
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
        
    # create method to format responses for existing task
    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete_status(self.completed_at)
        }
        
    # create method to return is_complete status dependent on completed_at data
    def is_complete_status(self, completed_at):
        if completed_at is None:
            return False
        else:
            return True
    
    # create class method to format responses for new task  
    @classmethod
    def from_dict(cls, task_request_data):
        return cls (
            title = task_request_data["title"],
            description = task_request_data["description"]
        )
        
    
