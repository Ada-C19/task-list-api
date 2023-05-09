from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)

    def to_dict(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
        return {
            "id": self.task_id, 
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" in task_data:
            completed_at = task_data["completed_at"]
        else:
            completed_at = None
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = completed_at
        )