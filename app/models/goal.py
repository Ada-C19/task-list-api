from app import db
from flask import abort, make_response, jsonify


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title
        )
    
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
