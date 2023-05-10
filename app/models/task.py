from app import db



class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column (db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),
        nullable=True)

    def to_dict(self):
        dictionary = { "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at != None}
        if self.goal_id: 
            dictionary["goal_id"] = self.goal_id
        return dictionary
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"], 
                            description=task_data["description"],
                            completed_at=task_data["completed at"])
        return task_data