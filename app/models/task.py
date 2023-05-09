from app import db
from flask import abort, make_response, jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

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

        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=is_complete,
        )
    
    def update_from_dict(self, task_data):
        try:
            self.title = task_data["title"]
            self.description = task_data["description"]
        except KeyError: 
            abort(make_response(jsonify({"details": "Invalid data"}), 400))
