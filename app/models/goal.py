from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)



    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(
            title=goal_data["title"]
        )

        return new_goal





    def to_dict_goal(self):
        return{ "goal": {
            "id":self.goal_id,
            "title":self.title}}