from app import db
from flask import make_response, abort, jsonify


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    @classmethod
    def from_dict(cls, goal_data):
        try:
            new_goal = Goal(title=goal_data["title"],
                            )
        except KeyError:
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
        
        return new_goal

    def to_dict(self):

        return dict(
            id=self.goal_id,
            title=self.title,
        )
    
    def update_from_dict(self, goal_data):
        try:
            self.title = goal_data["title"]
        except KeyError: 
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
