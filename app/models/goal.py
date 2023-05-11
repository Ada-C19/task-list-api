from app import db

class Goal(db.Model):
    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")
    

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }
    
    @classmethod
    def from_json(cls, request_body):
        return cls(
            title=request_body["title"]
            )
    
    