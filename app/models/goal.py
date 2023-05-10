from app import db
from flask import jsonify

# A Goal has many Tasks 

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
            }
        