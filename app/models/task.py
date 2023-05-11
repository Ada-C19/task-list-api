from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=None)

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title = task_title["title"],
            description = task_description["description"]
        )

        return new_task

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }