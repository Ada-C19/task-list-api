from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(300))
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal:
            task_dict["goal_id"] = self.goal_id

        return task_dict


    # @classmethod
    # def from_dict(cls, task_data):
    #     new_task = Task(title=task_data["title"], 
    #                     description=task_data["description"])   

    #     return new_task  
            
        