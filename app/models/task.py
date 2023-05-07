from app import db

class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    

    # def to_json(self):
    #         return dict(
    #             id=self.task_id,
    #             title = self.title,
    #             description = self.description,
    #             is_complete=self.completed_at is not None
    #         )
    
    # def __init__(self, title, description, completed_at=datetime.utcnow()):
    #     self.title = title
    #     self.description = description
    #     self.completed_at = completed_at


    







    
    
    
    
