from app import db


class Task(db.Model):
    """Task definition"""
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None) # set default value to <null>
    is_complete = db.Column(db.String, unique=False)    # designate as not completed

    def task_to_dict(self):
        """Create task as a dictionary"""
        task_as_dict = {}

        task_as_dict["task_id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["completed_at"] = self.completed_at
        task_as_dict["is_complete"] = self.is_complete

        return task_as_dict
    
    @classmethod
    def task_from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data["completed_at"],
                        is_complete=task_data["is_complete"])
        return new_task