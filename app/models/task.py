from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                    description=task_data["description"],
                    completed_at=None)
        return new_task
    
    
    def to_dict(self):
        if self.goal_id:

            return dict(
            id = self.task_id,
            goal_id = self.goal_id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )

        return dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )
    
    def is_task_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True
    


