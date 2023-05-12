from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    tasks = db.relationship("Task",back_populates="goal")

    def update_goal(self,request_body):
        self.title = request_body["title"]


    def to_dict(self):
        return{
            "id": self.goal_id,
            "title": self.title
        }


from app.models.goal import Goal
