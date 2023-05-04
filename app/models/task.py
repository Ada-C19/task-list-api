from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column()
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"]
        )

    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description
        )
