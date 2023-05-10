from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)  
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    
    def to_dict(self):
        task_as_dict = {}
        task_as_dict['id'] = self.task_id
        task_as_dict['title'] = self.title
        task_as_dict['description'] = self.description
        task_as_dict['is_complete'] = False
        if self.goal_id:
            task_as_dict['goal_id'] = self.goal_id 
        
        return task_as_dict
    
    @classmethod
    def from_dict(cls,task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"]
                        )
        return new_task