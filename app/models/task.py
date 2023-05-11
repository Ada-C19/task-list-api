from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
        }
    
    @classmethod
    def from_dict(cls, request_body):
        return cls(title=request_body.get("title"),
                description=request_body.get("description"),
                completed_at=request_body.get("completed_at"))
