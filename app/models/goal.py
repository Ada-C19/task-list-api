from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    # powerful takeaway: you can call a function on a value in a dict!
    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }
    
    

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(
            title=goal_data["title"]
        )
        return new_goal