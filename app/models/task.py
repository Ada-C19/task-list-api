from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        if not self.completed_at:

            return {
                "id" : self.task_id,
                "title" : self.title,
                "description" : self.description,
                "is_complete" : False
            }
              
    @classmethod
    def from_dict(cls, task_data):
        return Task(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data["completed_at"]
        )