from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy = True)

    # tasks = db.relationship("Task", back_populates="goal", lazy = True)

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])
        return new_goal
    
    def to_dict(self):
        return dict(
            id = self.goal_id,
            title = self.title)
    
    # def goal_task_dict(self):
    #     return dict(
    #         id = self.goal_id,
    #         task_ids = self.tasks
    #     )
