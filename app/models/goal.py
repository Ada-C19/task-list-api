from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates ="goal", lazy= True)
    

    def to_dict(self):
    
        goal_as_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        if self.tasks:
            goal_as_dict["task_ids"] = [task.to_dict() for task in self.tasks]

        return goal_as_dict


    def to_json(self):
        
        json_tasks = []
        
        for task in self.tasks:
            json_tasks.append(task.to_json())

        return{
            "id": self.goal_id,
            "title": self.title,
            "tasks": json_tasks
            }


    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"])
        return new_goal
