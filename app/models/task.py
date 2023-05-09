from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)
    goal = db.relationship("Goal", back_populates="task")
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"), nullable=True)
