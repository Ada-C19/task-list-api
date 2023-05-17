from app import db
from sqlalchemy.orm import relationship


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self, tasks=False):
        goal_dict = {
            "id": self.id,
            "title": self.title
        }

        if tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return goal_dict
    
