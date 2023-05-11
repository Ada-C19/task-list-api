from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    task = db.relationship("Task", back_populates="goals")

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.goal_id 
        goal_as_dict["title"] = self.title
    
        return goal_as_dict
    
    def to_goal_dict(self):
        task_in_goal_dict = {}
        task_in_goal_dict["id"] = self.goal_id
        task_in_goal_dict["task_ids"] = self.task_id
        
        return task_in_goal_dict

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(
                        title=goal_data["title"])
        return new_goal
    
    