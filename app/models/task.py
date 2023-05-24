from app import db

# create task model, define 'Task' using SQLAlchemy 
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(56))
    description = db.Column(db.String(200))
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back)
    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
            
        return task_dict