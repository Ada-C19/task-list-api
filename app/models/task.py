from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="taks")

    def to_dict(self):
        if not self.completed_at:
            return {
                "id" : self.task_id,
                "title" : self.title,
                "description" : self.description,
                "is_complete" : False
            }
        else:
            return {
                "id" : self.task_id,
                "title" : self.title,
                "description" : self.description,
                "is_complete" : True
            }

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title = task_data["title"],
            description = task_data["description"],
        )