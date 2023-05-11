from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    # Return the goal in a dictionary form (without task list)
    def to_dict(self):
        return {
            "id": self.goal_id, 
            "title": self.title
        }
    
    # Return the goal in dictionary form (with task list)
    def to_dict_with_tasks(self):
        task_list = []
        for task in self.tasks:
            task_list.append(task.to_dict_with_goal())

        dictionary = self.to_dict()
        dictionary["tasks"] = task_list
        
        return dictionary 
    
    # Create an instance of a goal using a dictionary
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title = goal_data["title"]
        )
