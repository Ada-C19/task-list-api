from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    # def goal_to_dict(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         }
    

    # @classmethod
    # def from_dict(cls, data):
    #     return cls(
    #         title = data["title"],
    #         description = data["description"],
    #         completed_at = data["completed_at"]
    #     )
