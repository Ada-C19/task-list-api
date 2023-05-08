from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        dict = {}
        dict["id"] = self.task_id
        dict["title"] = self.title
        dict["description"] = self.description
        if self.completed_at:
            dict["is_complete"] = True
        else:
            dict["is_complete"] = False

        return dict

    @classmethod
    def from_dict(self, data):
        return Task(
            title=data["title"],
            description=data["description"])
