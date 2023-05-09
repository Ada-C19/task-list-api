from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "task_ids": self.tasks #does this return a list of ids?
        }
    
    @classmethod
    def from_dict(cls, dict):
        new_goal = Goal(title=dict["title"])
        return new_goal