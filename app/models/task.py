from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)



    def to_dict(self):
        is_complete=True if self.completed_at else False 
        """
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
        """
        return{
            "id":self.task_id,
            "title":self.title,
            "description":self.description,
            "is_complete":is_complete
        }

#create function for title  & description
    @classmethod
    def create(cls, request_body):
        return cls(
            title = request_body["title"], 
            description = request_body["description"]
            )
    

#update function for title & description
    def update(self, request_body):
        self.title=request_body["title"]
        self.description=request_body["description"]
        

#patch function for is_completed
    def patch_complete(self):
        self.completed_at=datetime.utcnow()
    
#patch function for is_completed when incomplete
    def patch_incomplete(self):
        self.completed_at=None
    