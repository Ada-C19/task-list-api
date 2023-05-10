from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)




# Tasks should contain these attributes. Feel free to change the name of 
# the task_id column if you would like. The tests require the remaining columns 
# to be named exactly as title, description, and completed_at.

# task_id: a primary key for each task
# title: text to name the task
# description: text to describe the task
# completed_at: a datetime that has the date that a task is completed on. 
# Can be nullable, and contain a null value. A task with a null value for completed_at has not been completed. When we create a new task, completed_at should be null AKA None in Python.
