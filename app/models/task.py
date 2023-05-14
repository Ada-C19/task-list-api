from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }
        return task_as_dict

    # @classmethod
    # def from_dict(cls, task_data):
    #     return cls(title=task_data["title"], description=task_data["description"])