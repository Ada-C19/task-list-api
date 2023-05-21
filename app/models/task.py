from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    
    
    def to_dict(self):

        task_dict = dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    def is_task_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True
        
    @classmethod
    def from_dict(cls, task_dict):
        new_task = Task(
            title=task_dict["title"],
            description=task_dict["description"],
            )
        return new_task
    


