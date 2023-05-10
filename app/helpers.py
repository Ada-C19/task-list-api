from flask import jsonify, abort, make_response, request
from app.models.task import Task 
from app import db, token
import requests


def validate_model(cls, id):
    try:
        id = int(id)
    except:
        message = f"{cls.__name__} {id} is invalid"
        abort(make_response({"message": message}, 400))

    model = cls.query.get(id)

    

    if not model:
        message = f"{cls.__name__} {id} not found"
        abort(make_response({"message": message}, 404))

    return model

def slack_post_message(task):
    api_url = 'https://slack.com/api/chat.postMessage'

    payload = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task.title}"
    }

    headers = {
        'Authorization': f"Bearer {token}"
    }

    response = requests.post(api_url, headers=headers, data=payload)

    print(response.text)