from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_result(self): 
        is_complete = True
    
        if not self.completed_at:
            is_complete = False

        response = {"id": self.task_id, 
                "title": self.title, 
                "description": self.description,
                "is_complete": is_complete
                }
    
        if self.goal_id: 
            response["goal_id"] = self.goal_id
    
        return response 

    def to_dict(self): 
        return {"id": self.task_id, 
                "title": self.title, 
                "description": self.description,
                "completed_at": self.completed_at
                }
    
    # TODO - from_dict method
