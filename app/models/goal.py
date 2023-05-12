from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)


    @classmethod
    def from_dict_goals(cls, task_data):
        new_goal = Task(
            title = task_data["title"]
        )

        return new_task

    def to_dict_goals(self):
        return {
            "id": self.task_id,
            "title": self.title
        }
