from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    #had String(80) from Animals Sapphire Flasky
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)


    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": (self.completed_at!=None)
        }
