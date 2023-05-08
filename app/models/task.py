from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String, nullable=False)
    description= db.Column(db.String, nullable=False)
    completed_at= db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates= "tasks")
    goal_id= db.Column(db.Integer, db.ForeignKey('goal.goal_id'))

    def to_dict(self):
        as_a_dict = {}
        as_a_dict["id"] = self.task_id
        as_a_dict["title"] = self.title
        as_a_dict["description"] = self.description
        if self.completed_at == None:
            as_a_dict["is_complete"] = False
        else:
            as_a_dict["is_complete"] = True

        return as_a_dict