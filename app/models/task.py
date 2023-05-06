from app import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

def self_attributes(self):
    return set('title', 'description')

def to_dict(self):
    return {
        'title': self.title,
        'description': self.description,
        'completed_at': self.completed_at,
        'is_completed': self.is_completed
    }
    
@classmethod
def from_dict(cls, request_body):
    task = cls(
            title=request_body['title'],
            description=request_body['description'],
            completed_at=request_body['completed_at'],
            is_complete=request_body['is_complete'])
    return task