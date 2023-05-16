from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goals", lazy=True)

    def to_dic(self):
        goal_dic = {
        "goal": {
            "id": self.goal_id,
            "title": self.title
        }
    }
        return goal_dic
    
    def task_by_goal_id(self):
        tasks_by_goal_dic = {
        "id": self.goal_id,
        "title": self.title,
        "tasks": []
        }
        if self.tasks:
            for task in self.tasks:
                tasks_by_goal_dic["tasks"].append({
                    "id": task.task_id,
                    "goal_id": self.goal_id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": True if task.completed_at else False
                    })
        return tasks_by_goal_dic