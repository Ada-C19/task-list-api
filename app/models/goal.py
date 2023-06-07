from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    def to_dict(self):
        goal_dict = dict(
            id=self.id,
            title=self.title
        )
        if self.tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return goal_dict
    

    @classmethod
    def from_dict(cls, dict):
        new_goal = Goal(title=dict["title"])
        
        return new_goal