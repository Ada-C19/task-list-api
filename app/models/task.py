from app import db
# from sqlalchemy import Column, Integer, DateTime
# from sqlalchemy.sql import func

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["task_id"] = self.task_id
        goal_as_dict["title"] = self.title
        goal_as_dict["description"] = self.description
        goal_as_dict["completed_at"] = self.completed_at

        return goal_as_dict

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"],
                        description=goal_data["description"]
                        )
        return new_goal