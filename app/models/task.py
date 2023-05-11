from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable= False)
    description = db.Column(db.Text, nullable= False)
    completed_at = db.Column(db.DateTime, nullable= True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"],
            description = data_dict["description"],
            completed_at = data_dict.get("completed_at")
        )