from app import db
from flask import make_response, jsonify, abort
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def to_dict(self): 
        return {"task": {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }}
    

    def to_dict_with_goal_id(self): 
        task_dict = {
                "task_id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at is not None,
                "goal_id": self.goal_id 
        }
        return {"task": task_dict}

    


    @classmethod
    def from_dict(cls, data):
        title = data.get("title", "")
        description = data.get("description", "")
        completed_at = data.get("is_complete", None)
        return Task(title=title, description=description, completed_at=completed_at)


    @classmethod
    def validate_task(cls, task_id):
        try:
            task_id = int(task_id)
        except:
            abort(make_response(jsonify({"message": f"{cls.__name__} {task_id} invalid"}), 400))
    
        task = cls.query.get(task_id)

        if not task:
            abort(make_response(jsonify({"message": f"{cls.__name__} {task_id} not found"}), 404))

        return task
    
