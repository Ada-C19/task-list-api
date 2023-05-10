from app import db


class Task(db.Model):
    """Task definition"""
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None) # set default value to <null>
    is_complete = db.Column(db.String, default=False)    # designate as not completed

    @classmethod
    def task_from_dict(cls, task_data):
        """Input task as a dictionary. Assumes None/null for completed_at"""

        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data["completed_at"])
        return new_task
    
    def task_to_dict(self):
        """Output task information as a dictionary"""
        task_as_dict = {}

        task_as_dict["task_id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete

        return task_as_dict
    
    # def task_complete(self):
    #     if self.completed_at == None:
    #         self.is_complete = False
    #     else:
    #         self.is_complete = True
    