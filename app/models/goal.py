from flask import jsonify, request
from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(56))
    
    def to_dict(self):
        return{
            "id": self.task_id,
            "title": self.title,
        }
