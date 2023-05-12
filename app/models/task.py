from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer,primary_key=True,autoincrement = True) #autoincrement for the generated number
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime,default = None, nullable=True)
    goal = db.relationship("Goal",back_populates="tasks")
    goal_id_parent = db.Column(db.Integer,db.ForeignKey("goal.goal_id"))
    
    @classmethod
    def from_dict(cls,response_body):
        return cls(
            title=response_body["title"],
            description=response_body["description"]
        )
        
    def update_dict(self,request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        
    def update_dict(self,request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
    
    def to_dict(self):
        # is_complete= True if self.completed_at else False;
        dictionary = {}
        if self.goal:
            dictionary = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "goal_id": self.goal_id_parent,
            "is_complete": self.completed_at != None
        }

        else:
            dictionary = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
        }
    
        return dictionary


    def patch_complete(self):
        self.completed_at = datetime.utcnow()
    
    def patch_incomplete(self):
        self.completed_at = None