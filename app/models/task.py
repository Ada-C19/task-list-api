from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal = db.relationship("Goal", back_populates="tasks")
    goals_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))

    def to_dict(self):
        is_complete=True if self.completed_at else False 

        task_dict = {
            "id":self.task_id,
            "title":self.title,
            "description":self.description,
            "is_complete":is_complete
        }
        if self.goals_id:
            task_dict["goal_id"] = self.goals_id

        return task_dict

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
    