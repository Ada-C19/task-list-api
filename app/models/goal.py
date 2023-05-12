from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates ="goal", lazy= True)
    

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["goal_id"] = self.goal_id
        goal_as_dict["title"] = self.title

        return goal_as_dict
    
    def to_json(self):
        json_tasks = []
        
        for task in self.tasks:
            json_tasks.append(task.to_json())

        return{
            "id": self.goal_id,
            "title": self.title,
        }

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"])
        return new_goal
