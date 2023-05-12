from flask import make_response, abort
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__.lower()} {model_id} not found"}, 404))

    return model

def post_to_slack(task_title):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    data = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task_title}"
        }
    response = requests.post(url, headers=headers, data=data)
    return response