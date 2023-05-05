from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable = True)
    

    def task_display_dict(self):
        return{
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at,
            "is_complete": self.completed_at is not None
        }