from flask import Blueprint, request, make_response, jsonify, abort
# from ..models.task import Task
# from ..models.goal import Goal
# from app import db
# from datetime import datetime
import requests
import os
from flask import Flask 

# helper functions ==========================================
def validate_model(cls, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details" : f"It is not a valid id {task_id}"}, 400))
    response = cls.query.get(task_id)
    if not response:
        abort(make_response({"details" : f"{cls.__name__} #{task_id} not found"}, 404))
    return response


def send_requsest_to_slack(response_text):
    url = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("API_KEY")
    headers = {
        "Authorization" : API_KEY}
    
    data = {"channel": "#api-test-channel",
    "text" :  response_text}

    response = requests.post(url, headers=headers, json=data)
    return response