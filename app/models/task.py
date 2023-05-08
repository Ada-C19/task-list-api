from app import db
from flask import jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # SQLAlchemy supports nullable columns with specific syntax
    completed_at = db.Column(db.DateTime, nullable=True)

    # def to_dict(self):
    #     return jsonify (
    #         {"task":{
    #         "id": self.task_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": self.completed_at
    #         }})
    

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }
    
    # def to_dict(self):
    #     return jsonify (
    #         {
    #         "task": {
    #         "id": self.task_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": self.completed_at
    #     }})