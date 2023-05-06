from app import db
from flask import request, make_response, jsonify, abort
from sqlalchemy.exc import DataError
from datetime import datetime
import os
import requests
from dotenv import load_dotenv
load_dotenv()

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} invalid"
        abort(make_response({"error": message}, 400))

    model = cls.query.get(model_id)

    if not model:
        message = f"{cls.__name__} #{model_id} not found"
        abort(make_response({"error": message}, 404))

    return model

def send_slack_message(task_title):
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_title}"
    }

    response = requests.post(slack_url, headers=headers, data=data)
    return response

def create_item(cls):
    request_body = request.get_json()

    try: 
        new_item = cls.from_dict(request_body)
        db.session.add(new_item)
        db.session.commit()
        return make_response({cls.__name__.lower(): new_item.to_dict()}, 201)
    except KeyError as error:
        expected_keys = cls.get_required_fields()
        mising_keys = [key for key in expected_keys if key not in request_body]

        error = 'missing required valies'
        error_dict = {"error": error, "details": mising_keys}

        abort(make_response(error_dict, 400))
    except (TypeError, ValueError, DataError) as error_details:
        error = "Invalid request body"
        error_dict = {"error": error, "details": error_details}
        abort (make_response(error_dict, 400))        
    
def get_all_items(cls):
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        items = cls.query.order_by(cls.title.asc())
    elif sort_query == "desc":
        items = cls.query.order_by(cls.title.desc())
    else: 
        items = cls.query.all()

    if request.args.get("title"):
        items = items.filter(cls.title == request.args.get("title"))
        
    items_response = [item.to_dict() for item in items]
    return jsonify(items_response), 200

def get_item(cls, item_id):
    item = validate_model(cls, item_id)
    return make_response({cls.__name__.lower(): item.to_dict()}, 200)

def update_item(cls, item_id):
    item = validate_model(cls, item_id)
    item_data = request.get_json()

    for key, value in item_data.items():
        setattr(item, key, value)

    db.session.commit()
    
    return make_response({cls.__name__.lower(): item.to_dict()}, 200)

def delete_item(cls, item_id):
    item = validate_model(cls, item_id)

    db.session.delete(item)
    db.session.commit()

    details = f"{cls.__name__} {item.id} \"{item.title}\" successfully deleted"
    return make_response({"details": details}, 200)

def mark_item_complete(cls, item_id):
    item = validate_model(cls, item_id)

    item.completed_at = datetime.now()
    db.session.commit()

    send_slack_message(item.title)

    return make_response({cls.__name__.lower(): item.to_dict()}, 200)

def mark_item_incomplete(cls, item_id):
    item = validate_model(cls, item_id)

    item.completed_at = None
    db.session.commit()

    return make_response({cls.__name__.lower(): item.to_dict()}, 200)