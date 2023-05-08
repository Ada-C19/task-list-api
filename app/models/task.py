from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")
    is_complete = db.Column(db.Boolean, default=False)

    def to_dict(self):
        is_complete = False
        if self.completed_at is not None:
            is_complete = True
        if self.goal_id:
            return{
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
                }
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"], 
                        description=task_data["description"],
                        completed_at=None)

        if "completed_at" in task_data and task_data["completed_at"] is not None: 
            new_task.completed_at = task_data["completed_at"]
        
        return new_task
