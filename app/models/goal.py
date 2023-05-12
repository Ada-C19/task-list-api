from app import db
from app.models.task import Task
from app.tasks_routes import validate_model


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    title = db.Column(db.String, nullable = False)
    tasks = db.relationship("Task", back_populates = "goal", lazy = True)

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(
            title = goal_data.get("title")
        )
        return new_goal

    def to_dict(self, with_tasks=False):
        goals_dict = {
            "id": self.goal_id,
            "title": self.title, 
        }

        if with_tasks:
            tasks = []
            for task in self.tasks:
                task_as_dict = task.to_dict()
                task_as_dict["goal_id"] = self.goal_id
                tasks.append(task_as_dict)
            goals_dict["tasks"] = tasks

        return goals_dict
    
    def as_goal_dict(self):
        goal_dict = { "goal": self.to_dict()}
        return goal_dict
    
    def add_tasks_to_goal(self, task_ids):
        tasks = []
        for task_id in task_ids:
            task = validate_model(Task, task_id)
            tasks.append(task)
        self.tasks = tasks

    def get_task_ids(self):
        task_ids = [task.task_id for task in self.tasks]
        goal_and_task_dict = {
            "id": self.goal_id,
            "task_ids": task_ids
        }
        return goal_and_task_dict
    