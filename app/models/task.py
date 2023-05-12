from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True) 
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, dict_data):
        request_task = cls(title = dict_data["title"],
                    description = dict_data["description"],
                    completed_at = True if dict_data.get("completed_at") else None) 
        if dict_data.get("goal_id"):
            request_task.goal_id =  dict_data.get("goal_id")
        return request_task

             
        
    def to_dict(self):
        task_dict = {}
        task_dict = dict(id=self.task_id,
                    title=self.title,
                    description=self.description,
                    is_complete=  True if self.completed_at else False)
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict         

    


