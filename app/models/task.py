from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    

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
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            is_complete = task_data["is_complete"]
        )

    
    