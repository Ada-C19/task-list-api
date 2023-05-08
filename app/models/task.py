from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    #had String(80) from Animals Sapphire Flasky
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None) #None is og


    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": (self.completed_at!=None)
        }

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                        description=task_data["description"])
        return new_task