from sqlalchemy import DateTime
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = (self.completed_at != None)
    
        return task_as_dict
    

#poder usar el metodo de esta clase en create_book y retonarlo en esa 
# funcion en routes. Lo importante es el decorador y el cls
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        return new_task