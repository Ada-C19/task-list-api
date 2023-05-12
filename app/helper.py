from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import os
import requests
from dotenv import load_dotenv

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"details": "Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Data not found"}, 404))

    return model


def post_slack(task_title):
    url = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API_TOKEN_URI")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task_title}"
    }
    response = requests.post(url, headers=headers, data=data)
    return response




