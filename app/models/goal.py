from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self, tasks=False):
        goal_dict = {
            "id": self.id,
            "title": self.title
        }
        
        if tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]
        
        return goal_dict
    
    @classmethod
    def get_required_fields(self):
        return ["title"]
    
    @classmethod
    def from_dict(cls, goal_dict):
        return Goal(
            title=goal_dict["title"]
        )