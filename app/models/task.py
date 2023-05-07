from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
   

    def to_dict(self):
        return {"task_id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": (self.completed_at != None)} 
    
    @classmethod
    def from_dict(cls, task_data):
        new_planet = (name=task_data["title"], 
                            position=task_data["description"],
                            moon_count=task_data["complete_at"])
        return new_planet