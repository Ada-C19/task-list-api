from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    @classmethod
    def from_dict(cls, dict_data):
        return cls(title = dict_data["title"])
        
    
    def to_dict(self):
        return dict(id=self.task_id,
                    title=self.title)