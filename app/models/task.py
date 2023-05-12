from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)


    @classmethod
    def from_dict(cls, data_dict, date=None):
        
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=date
        )


    def to_dict(self):
        if not self.goal_id:
            return dict(
                id=self.task_id,
                title=self.title,
                description=self.description,
                is_complete=True if self.completed_at else False
            ) 
        else:
            return dict(
                id=self.task_id,
                title=self.title,
                description=self.description,
                is_complete=True if self.completed_at else False,
                goal_id=self.goal_id
            )     
