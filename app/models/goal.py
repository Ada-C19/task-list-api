from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    def to_dict(self):
        goal_dict=dict(
        id = self.id,
        title = self.title
        )
        return goal_dict