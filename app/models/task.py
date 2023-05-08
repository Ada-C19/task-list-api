from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(255))
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def from_dict(cls, task_details):
        new_task = cls(
            title=task_details["title"],
            description=task_details["description"],
            completed_at=task_details.get("completed_at", None)
        )

        return new_task

    # def to_dict(self):
    #     return {
    #         "id": self.task_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "completed_at": self.completed_at,
    #         "is_complete": self.is_complete
    #     }