from app import db
from flask import make_response, abort, jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(task):
        task_dict = dict(
                id=task.task_id,
                title=task.title,
                description=task.description,
                )
        
        if not task.completed_at:
            task_dict['is_complete'] = False
        else:
            task_dict['is_complete'] = True
            
        if task.goal_id:
            task_dict['goal_id'] = task.goal_id
            
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        try:
            new_task = Task(title=task_data["title"],
                            description=task_data["description"],
                            completed_at=None)
        except KeyError: 
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
        
        return new_task