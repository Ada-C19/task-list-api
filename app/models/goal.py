from app import db
class Goal(db.Model):
    
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    # Add the one-to-many relationship with Task
    tasks = db.relationship('Task', backref='goal', lazy=True)

    def to_dict(self):
        return {
            "goal_id": self.goal_id,
            "title": self.title
        }
