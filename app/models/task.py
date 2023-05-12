from app import db
from flask import make_response

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer,db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    #returning a dictionary from the database
    def task_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None}
    
        if self.goal_id:
             task_dict["goal_id"] =self.goal_id
        return task_dict
    
    
    #take data from user to make new task
    @classmethod 
    def from_dict(cls,request_data):
            return cls(
            title=request_data["title"],
            description=request_data["description"])
        
