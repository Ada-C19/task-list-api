from app import db
from flask import make_response, abort, jsonify


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(task):
        task_dict = dict(
                id=task.id,
                title=task.title,
                description=task.description,
                is_complete=task.completed_at != None,
                )
        
        if task.goal_id:
            task_dict['goal_id'] = task.goal_id
            
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        try:
            new_task = cls(title=task_data["title"],
                            description=task_data["description"],
                            completed_at=None)
        except KeyError: 
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
        
        return new_task
    
