from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default = None)
    # completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

        
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                    description=task_data["description"],
                    completed_at=None)
        # new_task = Task(title=task_data["title"],
        #                 description=task_data["description"],
        #                 completed_at=task_data["is_complete"])
        return new_task
    
    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_complete = self.is_task_complete()
        )
            # task_dict = {}
            # task_dict["id"] = self.id
            # task_dict["title"] = self.title
            # task_dict["description"] = self.description
            # task_dict["is complete"] = self.is_task_complete()
            
            # return task_dict
    
    def is_task_complete(self):
        if self.completed_at == None:
            self.completed_at = False
        else:
            self.completed_at = True
        return self.completed_at
