from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        task_dict = dict(
                id = self.id,
                title = self.title,
                description = self.description,
                completed_at = self.completed_at
            )   
        
        if self.completed_at:
            return task_dict
        else:
            task_dict["is_complete"] = False
            task_dict.pop("completed_at")
            return task_dict
    
    
    @classmethod
    def from_dict(cls, task_data):
        title = task_data["title"],
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

