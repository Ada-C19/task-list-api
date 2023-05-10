from app import db
from flask import abort, make_response


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"]
        )

    def to_dict(self):
        task_dict = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=bool(self.completed_at)
        )

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

