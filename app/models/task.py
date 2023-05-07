from app import db
# from sqlalchemy import Column, Integer, DateTime
# from sqlalchemy.sql import func

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["task_id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["completed_at"] = self.completed_at

        return task_as_dict

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"]
                        )
        return new_task