from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_dict(self):
        return {"id": self.goal_id,
                "title": self.title,} 

    @classmethod
    def from_dict(cls, task_data):
        new_goal = cls(title=task_data["title"])
        return new_goal
    
    def tasks_to_dict(self):
        return {
            "id": int(self.goal_id),
            "title": self.title,
            "tasks": [task.to_dict() for task in self.tasks]
        }