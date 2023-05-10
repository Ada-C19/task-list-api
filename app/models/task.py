from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default = None)
    
    def to_dict(self):
        if Task.completed_at is True:
            task_as_dict["is_completed"] == True
        else:  
            task_as_dict = {}
            task_as_dict["id"] = self.task_id
            task_as_dict["title"] = self.title
            task_as_dict["description"] = self.description
            task_as_dict["is_complete"] = (self.completed_at != None)

            return task_as_dict

    @classmethod
    def from_dict( cls,task_data):
            new_task = cls(title=task_data["title"],
                            description=task_data["description"])
            return new_task