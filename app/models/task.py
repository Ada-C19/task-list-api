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
            completed_at=task_details["completed_at"]
        )

        return new_task
