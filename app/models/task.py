from app import db
import pdb


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))
    goal = db.relationship("Goal", back_populates="tasks")
    

    def to_dict(self):
        is_complete = True
        if self.completed_at is None:
            is_complete = False
        return {
            "id" : self.task_id, 
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" in task_data:
            return cls(
                title = task_data["title"],
                description = task_data["description"],
                completed_at = task_data["completed_at"]
            )
        else:
            return cls(
                title = task_data["title"],
                description = task_data["description"]
            )


    
    