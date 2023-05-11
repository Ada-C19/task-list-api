from app import db
import types


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)


    @classmethod
    def show_required(cls):
        attributes = []

        for key, val in cls.__dict__.items():
            if key[:1] != "_" and "id" not in key:
                if not isinstance(val, (classmethod, types.FunctionType)):
                    attributes.append(key)

        return attributes


    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=None if not data_dict.get("completed_at") else data_dict["completed_at"]
        )


    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=True if self.completed_at else False
        )      
