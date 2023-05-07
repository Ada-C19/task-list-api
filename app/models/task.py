from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title= data_dict["title"],
            description= data_dict["description"],
        )