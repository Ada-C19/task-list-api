from app import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)
