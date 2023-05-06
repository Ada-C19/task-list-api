from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed_at': self.completed_at,
            'is_complete': self.is_complete
        }
    
    @classmethod
    def get_attributes(self):
        return 'title', 'description'
    
    @classmethod
    def from_dict(cls, request_body):
        if  not 'completed_at' in request_body:
            task = cls(
                    title=request_body['title'],
                    description=request_body['description'])
        else:
            task = cls(
                    title=request_body['title'],
                    description=request_body['description'],
                    is_complete=request_body['is_complete'],
                    completed_at=request_body['completed_at']) #func.now()??
        return task