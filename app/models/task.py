from app import db
from flask import abort, make_response, jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        try:
            new_task = Task(title=task_data["title"],
                            description=task_data["description"],
                            )
        except KeyError:
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
        
        return new_task

    def to_dict(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False

        task_dict = {}
        task_dict["id"] = self.task_id
        task_dict["title"] = self.title
        task_dict["description"] = self.description
        task_dict["is_complete"] = is_complete

        if self.goal:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    def update_from_dict(self, task_data):
        try:
            self.title = task_data["title"]
            self.description = task_data["description"]
        except KeyError: 
            abort(make_response(jsonify({"details": "Invalid data"}), 400))

    