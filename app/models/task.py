from app import db
from flask import Flask 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at= db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        task_as_dict={}
        
        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        if not self.completed_at:
            task_as_dict ["is_complete"] = False
        else: 
            task_as_dict ["is_complete"] = True

        return task_as_dict


    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"], 
                        description = task_data["description"],
                        #completed_at = task_data["is_complete"]
                        )
        return new_task

