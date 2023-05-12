from app import db
from app.models.goal import Goal
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
load_dotenv()

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable = True)
    goal = db.relationship("Goal", back_populates= "tasks")
    
    

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["task_id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["completed_at"] = self.completed_at
        if self.goal_id:
            task_as_dict["goal_id"] =self.goal_id

        return task_as_dict
    
    def to_json(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False

        if self.goal_id:
            return{
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete,
            "goal_id": self.goal_id
        }
        else:

            return{
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
        }
    

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"]
                        )
        return new_task
    
    def mark_complete(self, request_body):
        self.completed_at = datetime.utcnow()

    def mark_incomplete(self, request_body):
        self.completed_at = None
    
    def slack_mark_complete(self):
        API_KEY = os.environ.get("API_KEY")
        url = "https://slack.com/api/chat.postMessage"

        data = {
        "channel": "#task-list-api",
        "text": f"Someone just completed the task {self.title}"
        }
        headers = {
    'Authorization': f'{API_KEY}'
        }

        response = requests.post(url, headers=headers, data=data)

        print(response.text)