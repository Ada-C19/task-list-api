from app import db
import datetime 



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    # completed_at = db.Column(db.DateTime, default = None)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    # goal = db.relationship("Goal")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

        
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                    description=task_data["description"],
                    completed_at=None)
        return new_task
    
    
    def to_dict(self):
        if self.goal_id:

            return dict(
            id = self.id,
            goal_id = self.goal_id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )

        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )
    
    def is_task_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True
    
    from app.models.goal import Goal
    def to_goal_id_dict(self, goal_id):
        return dict(
            id = self.id,
            goal_id = goal_id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )
    # from app.models.goal import Goal
    # def to_dict_with_goal(self, goal_id):
    #     return dict(
    #         id = self.id,
    #         goal_id = int(goal_id),
    #         title = self.title,
    #         description = self.description,
    #         is_complete = self.is_task_complete()
    #     )
    
    

