from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    @classmethod
    def from_dict(cls, dict_data):
        return cls(title = dict_data["title"])
        
    def to_dict(self):
        return dict(id=self.goal_id,
                    title=self.title)
    
    def add_goal_keys(self, dict_data):
        return {
        "id": self.goal_id,
        "title": self.title,
        "tasks":dict_data}