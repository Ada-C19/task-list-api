from app import db
from flask import make_response

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    #returning a dictionary from the database
    def task_dict(self):
        return  {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": self.completed_at != None}
    
    
    #take data from user to make new task
    @classmethod 
    def from_dict(cls,request_data):
            return cls(
            title=request_data["title"],
            description=request_data["description"],
            completed_at=request_data.get("completed_at"))

        
