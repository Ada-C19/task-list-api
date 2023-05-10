from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean)

    def to_dict(self):
        random_bool = True
        if self.is_complete == True:
            random_bool = True
        else:
            random_bool = False
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            # In the Wave 1 test, they don't want completed_at in the response
            # completed_at=self.completed_at,
            # In the Wave 1 test, it wants is_complete to come back as True/False... in the db, this might be stored as "None" depending on the task
            is_complete=random_bool
        )
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title=task_data["title"], 
            description=task_data["description"]
            )
        return new_task