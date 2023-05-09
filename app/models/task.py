from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    #had String(80) from Animals Sapphire Flasky
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None) #None is og

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    # goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        updated_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": (self.completed_at!=None)}
        if self.goal_id:
            updated_dict["goal_id"] = self.goal_id
        return updated_dict
    

    @classmethod
    def from_dict(cls, task_data):
        # add all attributes
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        return new_task