from app import db
from flask import abort, make_response, jsonify
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False )
    completed_at = db.Column(db.DateTime, default = None, nullable = True)
    #child - many to one (the task are the children/ many children(tasks) to one parent(goal))
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_json(self):
        is_complete = True if self.completed_at else False;

        task_return = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

        if self.goal_id:
            task_return["goal_id"] = self.goal_id

        return task_return
    
    def update_dict(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]

    def patch_complete(self, request_body):
        self.completed_at = datetime.utcnow()

    def patch_incomplete(self,request_body):
        self.completed_at = None

    @classmethod
    def create_dict(cls, response_body):
        try:
            new_task = cls(
                title = response_body["title"],
                description = response_body["description"]
            )
        except KeyError:
            abort(make_response(jsonify({"details": "Invalid data"}), 400))                              
        return new_task