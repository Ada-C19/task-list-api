from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    #set many task to goal relationship
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),
        nullable=True)

    def to_dict(self):
        return {"id": self.task_id,
                "title": self.title,
                "goal_id": self.goal_id,
                "description": self.description,
                "is_complete": (self.completed_at!=None)} 
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                        description=task_data["description"])
        return new_task







