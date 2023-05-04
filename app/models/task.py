from app import db
from datetime import datetime


class Task(db.Model):
# task_id: a primary key for each task
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# title: text to name the task
    title = db.Column(db.String)
# description: text to describe the task
    description = db.Column(db.String)
# completed_at: a datetime that has the date that a task is completed on. Can be nullable, and contain a null value. A task with a null value for completed_at has not been completed. When we create a new task, completed_at should be null AKA None in Python.
    completed_at = db.Column(db.DateTime, nullable=True)

    def is_true(self):
        return bool(self.completed_at)