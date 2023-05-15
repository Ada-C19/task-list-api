from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self, tasks=False):

        build_dict = {
            "id": self.goal_id,
            "title": self.title
        }

        if tasks:
            build_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return build_dict
    
    @classmethod
    def from_dict(cls, build_dict):
        new_goal = cls(title=build_dict["title"])
        return new_goal
    
    # def from_dict(cls, build_dict):
    #     return Goal(
    #         title = build_dict["title"]
    #     )
    
