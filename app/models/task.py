from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        is_completed_flag = False
        if self.completed_at:
            is_completed_flag = True 
            
        return {
            "id" : self.task_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete": is_completed_flag}
    
    def to_dict_with_gold_id(self):
        is_completed_flag = False
        if self.completed_at:
            is_completed_flag = True 
            
        return {
            "id" : self.task_id,
            "goal_id" : self.goal_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete": is_completed_flag}
    
    @classmethod
    def from_dict(cls, task_data):
        if "completed_at" in task_data:
            new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data["completed_at"])
        else: 
            new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        return new_task