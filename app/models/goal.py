from app import db
from flask import make_response, abort, jsonify


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(goal):
        return dict(id=goal.goal_id, title=goal.title)
    
    @classmethod
    def from_dict(cls, goal_data):
        try:
            new_goal = Goal(title=goal_data["title"],)

        except KeyError: 
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
        
        return new_goal