from app import db
# from .goal import Goal


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return (dict(
                id=self.id,
                title=self.title
            ))
    
    # def to_dict_with_tasks(goal, self):
    #     # tasks_list = []
    #     # for task in goal.tasks:
    #     #     tasks_list.append(task.to_dict())

    #     # goal.tasks = tasks_list

    #     return dict(
    #             id=self.id,
    #             title=self.title
    #             tasks=Goal.tasks
    #         )
