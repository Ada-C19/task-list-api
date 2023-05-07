from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    # ADDING FOR WAVE 5 ???
    # goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    # goals = db.relationship("Goal", back_populates="task")

    def make_task_dict(self):
        return dict(
                id=self.task_id,
                title=self.title,
                description=self.description,
                is_complete=self.completed_at != None,  # if/else
            )