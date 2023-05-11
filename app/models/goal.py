from app import db

# "One" side
# one Goal has many Tasks
# tasks looks at the class Task and finds the value for attribute/column "goal"
# tasks attribute is pluralized bc a singular goal HAS MANY tasks
# db.relationship creates the join table
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    
    

    def to_dict(self, tasks=False):
        goal_dict = {
            "id": int(self.goal_id),
            "title": self.title
        }

        if tasks: 
            goal_dict["tasks"] = [tasks.to_dict() for task in self.tasks]

        return goal_dict


    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(
            title=goal_data["title"]
        )
        return new_goal