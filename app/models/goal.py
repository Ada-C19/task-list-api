from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
                "id": self.goal_id,
                "title": self.title
            }
        
    @classmethod
    def from_dict(self):
        return {
            "id": self.goal_id,
            "task_ids": [task.task_id for task in self.tasks]
        }