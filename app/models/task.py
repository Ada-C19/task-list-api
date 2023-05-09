from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer,primary_key=True,autoincrement = True) #autoincrement for the generated number
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime,default = None, nullable=True)
    
    def to_dict(self):
        is_complete= True if self.completed_at else False;

        return{
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

    @classmethod
    def create_dict(cls,response_body):
        return cls(
            title=response_body["title"],
            description=response_body["description"],
            # completed_at = response_body["completed_at"]
        )
    
    