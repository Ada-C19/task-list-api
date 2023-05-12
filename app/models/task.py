from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    is_complete = db.Column(db.DateTime, default=None)

    
    def to_dict(self):
        task_dict = dict(
                id = self.task_id,
                title = self.title,
                description = self.description,
                is_complete = self.is_complete
            )   

        if self.is_complete:
            task_dict["is_complete"] = True 

        else: 
            task_dict["is_complete"] = False

        return task_dict
    
    # @classmethod
    # def from_dict(cls, data_dict):
    #     return cls(
    #         title = data_dict["title"],
    #         description = data_dict["description"],
    #         is_complete = False 
    #         ) 
    

    
