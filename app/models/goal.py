from app import db
from flask import make_response, abort


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    @classmethod
    def from_dict(cls, data_dict):
        try:
            new_instance = cls(title=data_dict["title"])
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400))

        return new_instance
    
    def to_dict(self):
        goal_dict = dict(
            id=self.id,
            title=self.title
        )

        if self.tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]
        
        return goal_dict