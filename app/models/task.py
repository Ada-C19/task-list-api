from app import db

# Task is the child


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    # ADDING FOR WAVE 6 
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)



    def make_task_dict(self):
        task_dict = dict(
                id=self.task_id,
                title=self.title,
                description=self.description,
                is_complete=self.completed_at != None,
            )
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict