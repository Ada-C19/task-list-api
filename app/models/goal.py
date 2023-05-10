from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"])
    
    def to_dict(self):
        goal_dict = dict(
            id=self.id,
            title=self.title
        )

        if self.tasks:
            goal_dict["tasks"] = self.tasks
        
        return goal_dict