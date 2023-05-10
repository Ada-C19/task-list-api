from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
    
    def to_dict_with_task(self):
        task_list = []
        for task in self.tasks: 
            task_list.append(task.to_dict_with_goal())
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": task_list
        }
    
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title = goal_data["title"]
        )