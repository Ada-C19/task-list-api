from app import db

class Goal(db.Model):

    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
    

    # def to_json(self):
    #         return dict(
    #             id=self.task_id,
    #             title = self.title,
    #             description = self.description,
    #             is_complete=self.completed_at is not None
    #         )
    
    # def __init__(self, title, description, completed_at=datetime.utcnow()):
    #     self.title = title
    #     self.description = description
    #     self.completed_at = completed_at


    
