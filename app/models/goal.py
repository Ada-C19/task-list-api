from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])
        return new_goal
    
    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title)