from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable = True)
    

    def task_to_dict(self):
        return{
            "id": self.task_id,
            "title": self.title, 
            "description": self.description,
            "is_complete": self.completed_at is not None
      
        }
    

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data.get("completed_at", None)
        )

    
    
   
