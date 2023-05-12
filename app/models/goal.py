from app import db
from flask import abort, make_response

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_json(self):
        goal = {
            "id": self.id,
            "title": self.title
            }
        
        return goal

    @classmethod
    def from_json(cls, response_data):
        try:
            goal = cls(
                title = response_data["title"]
                )
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400))
        
        return goal
