from app import db
from flask import make_response, jsonify, abort
from datetime import datetime


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    tasks = db.relationship("Task", backref="goal", lazy=True)


    def to_dict(self):
        return {"goal": {
            "goal_id": self.goal_id,
            "title": self.title,
            }
        }


    @classmethod
    def from_dict(cls, data):
        title = data.get("title", "")
        return Goal(title=title)


    @classmethod
    def validate_goal(cls, goal_id):
        try:
            goal_id = int(goal_id)
        except:
            abort(make_response(jsonify({"message": f"{cls.__name__} {goal_id} invalid"}), 400))
    
        goal = cls.query.get(goal_id)

        if not goal:
            abort(make_response(jsonify({"message": f"{cls.__name__} {goal_id} not found"}), 404))

        return goal
    
