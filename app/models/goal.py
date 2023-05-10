from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref = "goal", lazy = True)
    #reminder == backref allows to access from tasks to goal - reverse relationship - access goal's tasks
    # lazy - Task obj be loaded as needed - prevents unnecessary queries - improves performance

    def goal_to_dict(self):
        return{
            "id": self.goal_id,
            "title": self.title
        }
    
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title=goal_data["title"],
        
        )



