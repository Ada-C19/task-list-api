from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, default=None) 
    
    @classmethod 
    def from_dict(cls, data_dict):
        return cls(title = data_dict["title"],
                description = data_dict["description"],
                completed_at = None)

    def to_dict(self):
        return dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = bool(self.completed_at)
        )

    
    
    



