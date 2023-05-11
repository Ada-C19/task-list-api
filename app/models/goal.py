from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title = data_dict["title"]
        )



    # def validate_complete(self):
    #     if self.completed_at:
    #         is_complete = True
    #     else:
    #         is_complete = False
    
    #     return {
    #         "id": self.task_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": is_complete
    #         }
    