from app import db
from flask import abort, make_response, jsonify

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)

    def to_json(self):
        return{
            "id": self.goal_id,
            "title": self.title
        }
    
    def update_dict(self, request_body):
        self.title = request_body["title"]
    
    @classmethod
    def create_dict(cls, response_body):
        try:
            new_goal = cls(
                title = response_body["title"]
            )
        except KeyError:
            abort(make_response(jsonify({"details": "Invalid data"}), 400))                              
        return new_goal