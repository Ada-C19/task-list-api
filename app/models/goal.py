from app import db
# Goal is the parent

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    
    tasks = db.relationship("Task", back_populates="goal", lazy=True)




    def make_goal_dict(self):
        return dict(
                id=self.goal_id,
                title=self.title,
            )
