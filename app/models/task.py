from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    #from_dict is replacing the writing each.
    def from_dict(self):
        is_complete = False
        if not self.completed_at:
            is_complete = False
        dic_data = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

        return dic_data