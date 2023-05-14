from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # tasks = db.relationship("Task",backref="goal", lazy = True)
    tasks = db.relationship("Task", back_populates="goal")

    # tasks = db.relationship("Task", back_populates="goal", lazy = True)

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])
        return new_goal
    
    def to_dict(self, tasks=False):

        if tasks:
            tasks_list = []
            for task in self.tasks:
                tasks_list.append(task.to_dict())
            return dict(
                id = self.goal_id,
                title = self.title,
                tasks = tasks_list
            )
        return dict(
            id = self.goal_id,
            title = self.title)
    
    # from app.models.task import Task
    
    # def connected_dict(self, task_data):
    #     return dict(
    #         id = self.goal_id,
    #         title = self.title,
    #         tasks = [
    #             dict(
    #         id = task_data["id"],
    #         goal_id = self.goal_id,
    #         title = task_data["title"],
    #         description = task_data["description"],
    #         completed_at = task_data["completed_at"]
    #         )
    #     ]
    # )
    