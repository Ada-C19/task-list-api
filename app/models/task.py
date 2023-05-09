from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer,primary_key=True,autoincrement = True) #autoincrement for the generated number
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime,default = None, nullable=True)
    
def to_dict(self):
    is_complete = True if self.completed_at else False;

    return{
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "completed_at": self.completed_at
    }

    # @classmethod
    # def from_dict(cls,data_dict):
    #     return cls(
    #         title=data_dict["title"],
    #         description=data_dict["description"],
    #         # completed_at = data_dict["completed_at"]
    #     )
    
    