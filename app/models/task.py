from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    # __tablename__ = "task"

    def to_dict(self):
        task_dict = dict(
                id = self.id,
                title = self.title,
                description = self.description
            )
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        if self.completed_at:
            task_dict["is_complete"] = True
        else:
            task_dict["is_complete"] = False
        
        return task_dict
    
    
    @classmethod
    def from_dict(cls, task_data):
        title = task_data["title"]
        description = task_data["description"]
    
        if "completed_at" in task_data:
            completed_at = task_data["completed_at"]
            return cls(
                title=title,
                description=description,
                completed_at=completed_at
            )
        else:
            return cls(
                title=title,
                description=description
            )

