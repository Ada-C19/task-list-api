from flask import abort, make_response
from datetime import datetime
import os, requests

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model


def update_model(model, request_body):
    if "completed_at" in request_body:
        try:
            request_body["completed_at"] = datetime(request_body["completed_at"])
        except TypeError:
            abort(make_response({"details": "Invalid data"}, 400))
    for attribute, value in request_body.items():
        try:
            setattr(model, attribute, value)
            # setattr() is a built-in Python function that sets the value of 
            # a named attribute of an object. It takes 3 arguments: the object to modify,
            # the name of the attribute to set, and the value to set 
        except KeyError:
            return abort(make_response({"details": "Invalid data"}, 400))


def create_model(cls, request_body):
    try:
        model = cls.from_dict(request_body)
    except (KeyError, TypeError):
        return abort(make_response({"details": "Invalid data"}, 400))
    return model


def sort_models(cls, models, sort_query):
    if sort_query == "desc":
        models = models.order_by(cls.title.desc()).all()
    elif sort_query == "asc":
        models = models.order_by(cls.title.asc()).all()
    else: # sort models by id in ascending order by default
        models = models.order_by(cls.id.asc()).all()
    return models 


def send_slack_message(task):
    token = os.environ.get("SLACK_BOT_TOKEN")
    external_url = 'https://slack.com/api/chat.postMessage'
    headers = {"Authorization": f"Bearer {token}"}
    data = {"channel": "task-notifications", 
            "text": f"Someone just completed the task \"{task.title}\""}
    response = requests.post(external_url, headers=headers, json=data)
    return response