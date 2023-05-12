from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer,primary_key=True,autoincrement = True) #autoincrement for the generated number
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime,default = None, nullable=True)
    # goal = db.relationship("Goal",back_populates="goals")
    # goal_id = db.Column(db.Integer,db.ForeignKey("goal_id"))
    
    def to_dict(self):
        is_complete= True if self.completed_at else False;

        return{
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

    def update_dict(self,request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
    
    @classmethod
    def create_dict(cls,response_body):
        return cls(
            title=response_body.get("title"),
            description=response_body.get("description"),
            # completed_at = response_body.get("completed_at",None)
        )
    
    def patch_complete(self):
        self.completed_at = datetime.utcnow()
    
    def patch_incomplete(self):
        self.completed_at = None