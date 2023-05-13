from app import db
from sqlalchemy import desc, asc
from flask import make_response, abort, request
from app.models.task import Task
from app.models.goal import Goal
import requests
import os

## Helper Functions
# Validate ID function
def validate_model(cls, model_id):
    model_item = cls.query.get(model_id)

    if not model_item:
        return abort(make_response({"message": f"{cls.__name__} with ID {model_id} not found."}, 404))

    return model_item

# Sort results
def query_sort(cls):
    query_sort = request.args.get("sort")

    if query_sort == "asc":
        model_items = db.session.query(cls).order_by(asc(cls.title)).all()
    elif query_sort == "desc":
        model_items = db.session.query(cls).order_by(desc(cls.title)).all()
    else:
        model_items = cls.query.all()

    return model_items

# Filter results
def filter_results(cls):
    title_query = request.args.get("title")

    if title_query:
        model_items = cls.query.filter_by(title=title_query)
    else:
        model_items = cls.query.all()

    return model_items

# Sort and filter results
def filter_and_sort(cls):
    model_items = filter_results(cls)

    return query_sort(cls)

def send_slack_message(cls):
    key = os.environ.get("key")
    url_path = "https://slack.com/api/chat.postMessage"
    body = {
        "channel": "C056TH84MSN",
        "text": f"{cls.__name__} '{cls.title}' has been completed! Well done!"
    }
    header = {
        "Authorization": f"Bearer {key}"
    }
    
    try:
        slack = requests.post(url_path, headers=header, json=body)
    except:
        pass