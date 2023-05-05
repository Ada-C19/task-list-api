from app import db 
from app.models.goal import Goal

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String, nullable = False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def response_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at != None else False
        }

        return task_dict 