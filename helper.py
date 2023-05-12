from flask import make_response, abort
import requests
import json
import os


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        message = {"message": f"Invalid {cls.__name__} id {model_id}"}
        abort(make_response(message, 400))

    model = cls.query.get(model_id)

    if not model:
        message = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(message, 404))
    else:
        return model


def send_slack_massage(task):
    SLACK_POST_ENDPOINT = "https://slack.com/api/chat.postMessage"
    SLACK_API = os.environ.get("SLACK_API")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_API}"
    }

    slack_post_data = json.dumps({
        "text": f"Someone just completed the task {task.title}",
        "channel": "C05769EL4RF",
    })

    requests.post(
        url=SLACK_POST_ENDPOINT, headers=headers, data=slack_post_data)
