from app import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    __tablename__ = "goal"

    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title
        )
    
    @classmethod
    def from_dict(cls, goal_data):
        title = goal_data["title"]
        return cls( title=title )

    
    
