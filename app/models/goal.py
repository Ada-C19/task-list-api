from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    #task = db.relationship("task", back_populate="task")

    def to_dict(self):
        return {"id": self.goal_id,
                "title": self.title,
} 
    
    @classmethod
    def from_dict(cls, task_data):
        new_goal = cls(title=task_data["title"])
        return new_goal