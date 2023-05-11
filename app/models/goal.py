from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True) 
    # lazy is set to True by default. explicitly set to True here for learning's sake :) related models will
    # only be loaded when access is needed, which can improve performance 

    def to_dict(self):
        return dict(
                id=self.id,
                title=self.title
                )

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(title=goal_data["title"])


