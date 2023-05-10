from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # FROM_DICT (request)
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )

    # TASK TO_DICT (response should be a dict that is the value of key "task" in a dict)
    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.completed_at != None

        return task_as_dict


    # def make_task_dict(self):
    #     return dict(id=self.task_id,
    #         title=self.title,
    #         description=self.description,
    #         is_complete=self.completed_at != None)