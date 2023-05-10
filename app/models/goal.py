from app import db
from flask import abort, make_response, jsonify


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        goal_dict =  dict(
            id=self.goal_id,
            title=self.title
        )

        if self.tasks:
            goal_dict["tasks"] = self.tasks

        return goal_dict
    
    @classmethod
    def from_dict(cls, data):
        return Goal(
            title = data["title"]
        )
    
    @classmethod
    def validate_model(cls, model_id):
        try:
            model_id = int(model_id)
        except ValueError:
            abort(make_response(jsonify({"details": f"{cls.__name__} {model_id} invalid"}), 400))
        
        model = cls.query.get(model_id)
        if not model:
            abort(make_response(jsonify({"details": f"{cls.__name__} {model_id} not found"}), 404))

        return model
