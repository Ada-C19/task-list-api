from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    # Return the Task in dictionary form (without goal id)
    def to_dict(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
        return {
            "id": self.task_id, 
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    # Return the Task in dictionary form (with goal id)
    def to_dict_with_goal(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
        return {
            "id": self.task_id, 
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete,
            "goal_id": self.goal_id
        }
    
    # Create an instance of a Task using a dictionary
    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" in task_data:
            completed_at = task_data["completed_at"]
        else:
            completed_at = None
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = completed_at
        )