from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        goal_dict = dict(
            id = self.task_id,
            title = self.title,
        )
        if self.tasks:
            goal_dict["tasks"] = self.tasks

        return goal_dict



    @classmethod
    def from_dict(cls,task_data):
        new_goal = Goal(
            title = task_data["title"]
        )
