from app import db
from flask import abort, make_response

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)

    def to_json(self):
        task = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": True
        }
        
        if not self.goal_id and not self.completed_at:
            task["is_complete"] = False
        
        elif self.goal_id:
            task["goal_id"] = self.goal_id
            if self.completed_at == None:
                task["is_complete"] = False

        return task

    @classmethod
    def from_json(cls, response_data):
        try:
            task = cls(
                title = response_data["title"],
                description = response_data["description"]
                )
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400))
        
        return task
