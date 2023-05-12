from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        goal_dict =  dict(
            id=self.goal_id,
            title=self.title
        )

        if self.tasks:
            goal_dict["tasks"] = self.tasks

        return goal_dict
    
    @classmethod
    def from_dict(cls, data):
        return Goal(
            title = data["title"]
        )

