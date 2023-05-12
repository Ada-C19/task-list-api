from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    @classmethod
    def goal_from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"])
        return new_goal
    
    def goal_to_dict(self):
        goal_as_dict = {}

        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title
        if self.tasks:
            task_list = []
            for task in self.tasks:
                task_list.append(task.task_to_dict(self))
                goal_as_dict["tasks"] = task_list
            
        return goal_as_dict
    
    def goal_to_dict_with_task(self):
        goal_as_dict = {}

        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title
        goal_as_dict["tasks"] = self.tasks

        return goal_as_dict