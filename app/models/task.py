from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def from_dict(cls, dict_data):
        return cls(title = dict_data["title"],
                   description = dict_data["description"] #completed_at = dict_data["completed_at"]
                   )
    
    def to_dict(task):
        return dict(id=task.id,
                    title=task.title,
                    description=task.description,
                    completed_at=task.completed_at)