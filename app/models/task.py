from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.Integer, nullable = True)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at
        }

    def to_dict_task(self):
        return {
            "task": {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at
            }
        }