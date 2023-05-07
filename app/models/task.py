from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed_at = None

    def to_json(self):
            return {
            'task_id': self.task_id,
            'description': self.description,
            'completed_at': self.completed_at,
            }
    