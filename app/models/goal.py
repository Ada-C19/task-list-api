from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):   
        #tasks = [task.to_dict() for task in self.tasks]
        return {
            "id" : self.goal_id,
            "title" : self.title
            
        }
    def to_dict_with_tasks(self):
        tasks = [task.to_dict_with_goal() for task in self.tasks]
        return {
            "id" : self.goal_id,
            "title" : self.title,
            "tasks" : tasks
        }
