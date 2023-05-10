from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_result(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
    
    def to_result_with_tasks(self):
        response = []
        for task in self.tasks:
            response.append(task.to_result())
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": response
        }