from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        self_dict = {}
        self_dict["id"] = self.task_id
        self_dict["title"] = self.title
        self_dict["description"] = self.description
        self_dict["is_complete"] = self.completed_at is not None

        return self_dict
        # return {
        #     "id": self.task_id,
        #     "title": self.title,
        #     "description": self.description,
        #     "is_complete": self.completed_at is not None,
        #     }