from flask import jsonify, abort, make_response, request
from app.models.task import Task
from dotenv import load_dotenv
import requests
from datetime import datetime
from app import db
import os

load_dotenv()

def send_slack_message(completed_task):
    TOKEN = os.environ['SLACK_API_TOKEN']
    AUTH_HEADERS = {
        "Authorization": f"Bearer {TOKEN}"
    }
    CHANNEL_ID = "C0561UUDX4K"
    SLACK_URL = "https://slack.com/api/chat.postMessage"

    try:
        message = f"Someone just completed the task {completed_task.title}"
        payload = {
            "channel": CHANNEL_ID,
            "text": message
            }
    
        requests.post(SLACK_URL, data = payload, headers = AUTH_HEADERS)
    
    except:
        print("There was an error making the call to Slack")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        message = {"details": "Invalid data"}
        abort(make_response(message, 404))

    return model


def create_item(cls):

    request_body = request.get_json()

    try:
        new_item = cls.from_dict(request_body)
        db.session.add(new_item)
        db.session.commit()
        return make_response({cls.__name__.lower(): new_item.to_dict()}, 201)
    except:
        return make_response({"details": "Invalid data"}, 400)
    


def get_all_items(cls):

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        items = cls.query.order_by(cls.title)
    
    elif sort_query == "desc":
        items = cls.query.order_by(cls.title.desc())

    else:
        items = cls.query.all()

    if request.args.get("title"):
        items = cls.query.filter(cls.title== request.args.get("title"))

    items_response = []
    for item in items:
        items_response.append(item.to_dict())

    return jsonify(items_response), 200


def get_one_item(cls, model_id):

    item = validate_model(cls, model_id)
    return make_response({cls.__name__.lower(): item.to_dict()}), 200
    

def update_item(cls, model_id):
    try:
        item = validate_model(cls, model_id)
        request_body = request.get_json()
        
        for key, value in request_body.items():
            setattr(item, key, value)

        db.session.commit()

        return make_response({cls.__name__.lower(): item.to_dict()}, 200)
    
    except:
        return jsonify({"Message": "Invalid id"}), 404
    

def delete_item(cls, model_id):

    item = validate_model(cls, model_id)

    db.session.delete(item)
    db.session.commit()

    message = {"details": f"{cls.__name__} {model_id} \"{item.title}\" successfully deleted"}
    return make_response(message, 200)


def mark_item_complete(cls, model_id):
    try:
        new_item = validate_model(cls, model_id)
    except:
        return jsonify({"Message": "Invalid id"}), 404
    
    new_item.completed_at = datetime.utcnow()

    send_slack_message(new_item)

    db.session.commit()

    return jsonify({"task": new_item.to_dict()}), 200


def mark_item_incomplete(cls, model_id):

    try:
        new_item = validate_model(cls, model_id)
    except:
        return jsonify({"Message": "Invalid id"}), 404

    new_item.completed_at = None
    
    db.session.commit()

    return jsonify({"task": new_item.to_dict()}), 200

