from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])
        return new_goal
    
    def to_dict(self, tasks=False):

        build_dict = {
            "id": self.goal_id,
            "title": self.title
        }

        if tasks:
            build_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return build_dict
