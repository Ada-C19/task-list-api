from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates='goal')

    def to_dict(self):
        goal_dict = {"id": self.goal_id,
                    "title": self.title}
        return goal_dict


    @classmethod
    def from_dict(cls, dict):
        return Goal(title=dict['title'])
    
    def to_dict_with_tasks(self):
        tasks = []
        for task in self.tasks:
            tasks.append(task.to_dict())
        return {"id": self.goal_id,
                "title": self.title,
                "tasks": tasks}
    