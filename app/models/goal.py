from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def goal_to_dict(self):
            return {
            "id": self.goal_id,
            "title": self.title
            }
    @classmethod
    def create_new_goal(cls, request_data):
        if "title" not in request_data:
            raise KeyError
       
        return cls(
            title=request_data["title"].title()
        )
    
    def __str__(self):
        return {
            self.__class__.__name__.lower(): {
                "id": self.goal_id,
                "title": self.title
            }
        }
    
    def update(self, goal):
        for key, value in goal.items():
            if key == "title":
                self.title = value
        
        return self.goal_to_dict()

