from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Converts Task model into a dict
    def to_dict(self):
        is_complete = False
        if self.completed_at:
            is_complete = True
        dic_data = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

        return dic_data
    
    # Will take in a dict and return a new Task instance
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
        title= task_data["title"],
        description= task_data['description'],
        completed_at= task_data['completed_at'])

        return new_task
