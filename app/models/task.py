from sqlalchemy import DateTime
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        return {"id":self.id,
                "title": self.title,
                "description": self.description,
                "completed_at":self.completed_at}
