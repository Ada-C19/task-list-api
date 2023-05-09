from app import db
from app.models.task import Task

class Goal(db.Model):

    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', backref='goal', lazy=True)


    def to_dict(self):
        goal_as_dict={}
        
        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title
        return goal_as_dict
    
  
##### REFACTOR AND USE FUNCTION FROM ABOVE 
    def to_dict_with_tasks(self):
        goal_as_dict={}
        
        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title

        tasks_dicts = []
        for task in self.tasks:
            tasks_dicts.append(task.to_dict())

        goal_as_dict["tasks"] = tasks_dicts

        return goal_as_dict


    @classmethod
    def from_dict(cls, goal_data):
        new_goal =  Goal(title=goal_data["title"])
        return new_goal
