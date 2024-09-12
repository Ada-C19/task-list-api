from flask import abort, make_response
import requests
import os

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def create_slack_message(task):
    api_url = "https://slack.com/api/chat.postMessage"
    TOKEN = os.environ.get("SLACK_API_KEY") 

    payload = {
    "channel": "#api-test-channel",
    "text": f"Someone just completed the task {task.title}."
    }
    headers = {
    'Authorization': f"Bearer {TOKEN}"
    }

    response = requests.post(api_url, headers=headers, data=payload)

    print(response.text)

