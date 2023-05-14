from app import db
import datetime 



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    # completed_at = db.Column(db.DateTime, default = None)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

        
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                    description=task_data["description"],
                    completed_at=None)
        return new_task
    
    # @classmethod
    # def from_dict(cls, request_body):
    #     return cls(
    #         title = request_body["title"],
    #         description = request_body["description"],
    #         completed_at = request_body.get("completed_at"),
    #         goal_id = request_body.get("goal_id")
    #     )
    
    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )
    

    
    def is_task_complete(self):
        if self.completed_at == None:
            self.completed_at = False
        else:
            self.completed_at = True
        return self.completed_at
    

