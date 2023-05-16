from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
import requests

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


def post_slack_message(task_title):
    slack_url = "https://slack.com/api/chat.postMessage"
    channel_id = "task-notifications"
    slack_message = f"Someone just completed the task {task_title}"
    headers = dict(
        Authorization = os.environ.get("SLACK_AUTH")
    )
    data = dict(
        channel = channel_id,
        text = slack_message
    )
    response = requests.post(slack_url, headers=headers, data=data)
    return response