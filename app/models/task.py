from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=255))
    description=db.Column(db.String)
    completed_at=db.Column(db.DateTime, nullable=True)
    is_complete= db.Column(db.Boolean, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def task_to_dict(self):
        return {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": False if self.completed_at is None else True
        if self.completed_at is not None else None
        }
    
    @classmethod
    def create_new_task(cls, request_data):
        if "title" not in request_data:
            raise KeyError({"details": "Invalid data"})
        if "description" not in request_data:
            raise KeyError("description")
        
        request_data["completed_at"] = None
        is_complete = False if request_data["completed_at"] is None else True
        
        return cls(
            title=request_data["title"].title(),
            description=request_data["description"],
            completed_at=request_data.get("completed_at"),
            is_complete=is_complete
        )
      
    def update(self, task):
        for key, value in task.items():
            if key == "title":
                self.title = value
            if key == "description":
                self.description = value
        
        return self.task_to_dict()
    
    def __str__(self):
        return {
            self.__class__.__name__.lower(): {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
            }
        }
