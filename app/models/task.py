from app import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=True)
    goal = db.relationship('Goal', back_populates='tasks')

    def to_dict(self):
        task_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.is_complete
            }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
    
        return task_dict
    
    #returns all the attributes that must be passed in order to create a record. All not nullable instance variables accept id.'
    @classmethod
    def get_attributes(cls):
        return 'title', 'description'
    
    @classmethod
    def from_dict(cls, request_body):
        task = cls(
                title=request_body['title'],
                description=request_body['description'],
                is_complete=request_body.get('is_complete', False),
                completed_at=request_body.get('completed_at', None),
                goal_id=request_body.get('goal_id', None))
        return task