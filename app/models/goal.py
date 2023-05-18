from app import db

class Goal(db.Model):
    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")
    

    def to_json(self, tasks=False):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        if tasks:
            goal_dict["tasks"] = [task.to_json() for task in self.tasks]
        return goal_dict
    
    @classmethod
    def from_json(cls, request_body):
        return cls(
            title=request_body["title"]
            )
    
