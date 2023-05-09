from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True) #,

    @classmethod
    def from_dict(cls, dict_data):
        return cls(title = dict_data["title"],
                description = dict_data["description"],
                 completed_at = True if dict_data.get("completed_at") else None) #None)# dict_data["completed_at"]
        
    
    def to_dict(self):
        return dict(id=self.task_id,
                    title=self.title,
                    description=self.description,
                    is_complete=  True if self.completed_at else False)#False) #task.completed_at
        # return {"task":dict(id=self.task_id,
        #             title=self.title,
        #             description=self.description,
        #             is_complete=False)}#task.completed_at
    def add_task_key(dict_data):
        return {"task":dict_data}