from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)


    def to_dict(self):
        return {
            "id" : self.goal_id,
            "title" : self.title
        }
    
    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title = goal_data["title"]
        )