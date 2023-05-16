from app import db
from flask import make_response, abort
import os, requests


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

def slack_bot_message(message):
    slack_api_key = os.environ.get("SLACK_BOT_TOKEN")
    slack_url = "https://slack.com/api/chat.postMessage"
    header = {"Authorization": slack_api_key}

    slack_query_params = {
        "channel": "task-notifications",
        "text": message
    }
    print(slack_api_key)
    requests.post(url=slack_url, data=slack_query_params, headers=header)