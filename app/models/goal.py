from app import db
from app.routes import validate_model

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates = "goal", lazy=True)

    def to_dict(self):  
        return {
            "id" : self.goal_id,
            "title" : self.title
            }
    
    def to_dict_with_tasks(self): 
        task_list = []
        for task in self.tasks:
            task_list.append(task.to_dict_with_gold_id())
        return {
            "id" : self.goal_id,
            "title" : self.title,
            "tasks" :task_list
            }
    
    
    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"])
        return new_goal