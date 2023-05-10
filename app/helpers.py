from flask import Blueprint, make_response, abort, request, jsonify
from app.models.task import Task 
from app.models.goal import Goal 
from app import db
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")



#In this file I will implements all the helper functions needed from routes.py

def post_to_slack(task_title):
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "channel": "task-notification",
        "text": f"Someone just completed the task {task_title}"
    }

    response = requests.post(slack_url, headers=headers, data=data)
    return response




def validate_model(cls, model_id):
    try:
        model_id = int(model_id)

    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model 


def delete_model(cls, model_id):
    model = validate_model(cls,model_id)
    db.session.delete(model)
    db.session.commit()
    return make_response({"details": f'{cls.__name__} {model_id} "{model.title}" successfully deleted'})


def read_one_model(cls, model_id):
    model = validate_model(cls, model_id)
    return make_response({cls.__name__.lower(): model.to_dict()}, 200)


def create_new_model(cls, model_data):
    try: 
        new_model = cls.from_dict(model_data)
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))
    db.session.add(new_model)
    db.session.commit()
    return make_response({cls.__name__.lower():new_model.to_dict()}, 201)
