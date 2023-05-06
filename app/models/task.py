from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        if not self.completed_at:
            return {
                "task": {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": False
                }
            }
        else:
            return {
                "task": {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": True
                }
            }
         
    @classmethod
    def from_dict(cls, task_dict):
        if not task_dict.get("completed_at"):
            return cls(title=task_dict["title"],
                       description=task_dict["description"],
                       completed_at=None)
        else:
            return cls(title=task_dict["title"],
                       description=task_dict["description"],
                       completed_at=task_dict["completed_at"])
