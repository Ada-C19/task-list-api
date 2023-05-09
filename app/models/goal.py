from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    def to_dict(self):
        goal_dict = {   
        "id": self.goal_id,
        "title": self.title
        }
        if self.tasks:
            goal_dict["tasks"] = self.tasks
        
        return goal_dict