from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)

    def to_dict(self):
        if self.completed_at != None:
            is_complete = True
        else:
            is_complete = False
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

    def to_dict_task(self):
        if self.completed_at != None:
            is_complete = True
        else:
            is_complete = False
        return {
            "task": {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
            }
        }
    
    def mark_complete(self, is_complete):
        if is_complete:
            self.completed_at = datetime.utcnow()
        else:
            self.completed_at = None
        db.session.commit()