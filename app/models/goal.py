from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)

    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return { 
            "id": self.goal_id,
            "title": self.title,
        }


    @classmethod
    def from_dict(cls,goal_details):
        new_goal = Goal(title=goal_details["title"])
        return new_goal
    
    