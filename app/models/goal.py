from app import db
from flask import Blueprint, jsonify, make_response, abort, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

class Goal(db.Model):

    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):

        goal_dict = {
            "id": self.goal_id,
            "title": self.title
        }

        return goal_dict

    @classmethod

    def from_dict(cls, goal_dict):

        if "title" not in goal_dict:
            abort(make_response(jsonify({"details": "Invalid data"}), 400))

        return cls(title=goal_dict["title"])


