from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) #when refactoring change to varchar
    description = db.Column(db.String) # when refacoring change to varvhar
    completed_at = db.Column(db.DateTime, default=None, nullable=True) 
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data["completed_at"]
        )

        return new_task





    def to_dict(self):
        return{"task": {
            "id":self.task_id,
            "title":self.title,
            "description":self.description,
            "is_complete": True if self.completed_at else False}}
# wave 1
#Our task list API should be able to work with an entity called Task.
# Tasks are entities that describe a task a user wants to complete. They contain a:
# title to name the task
# description to hold details about the task
# an optional datetime that the task is completed on
# Our goal for this wave is to be able to create, read, update, and delete different tasks. 
# We will create RESTful routes for this different operations.


