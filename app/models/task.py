from app import db
from flask import abort, make_response, jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks", lazy=True)

    def to_dict(self):
        task_dict =  dict(
            id= self.task_id,
            title = self.title,
            description = self.description,
            is_complete = True if self.completed_at else False
        )

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    @classmethod
    def from_dict(cls, data):
        return Task(
            title = data["title"],
            description = data["description"],
            completed_at = data.get("is_complete", None),
            goal_id = data.get("goal_id", None)
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
