from app.models.task import Task
from flask import jsonify, abort, make_response
from app import token
import requests

def filter_by_params(cls, query_params):
    sort_by = query_params.get("sort")
    
    if sort_by:
        return get_sorted_items_by_params(cls, query_params)
    
    if query_params:
        query_params = {k.lower(): v.title() for k, v in query_params.items()}
        items = cls.query.filter_by(**query_params).all()
    else:
        items = cls.query.all()
    
    return items

def get_sorted_items_by_params(cls, query_params):
    sort_param = query_params.pop('sort', None)

    if sort_param == 'asc':
        return cls.query.filter_by(**query_params).order_by(cls.title.asc()).all()
    elif sort_param == 'desc':
        return cls.query.filter_by(**query_params).order_by(cls.title.desc()).all()
    else:
        return cls.query.filter_by(**query_params).order_by(cls.id.asc()).all()

    
def validate_model(cls, id):
    try:
        id = int(id)
    except:
        message = f"{cls.__name__} {id} is invalid"
        abort(make_response({"message": message}, 400))

    obj = cls.query.get(id)
    if not obj:
        abort(make_response(jsonify(message=f"{cls.__name__} not found"), 404))
    
    return obj

def slack_post_message(task):
    api_url = 'http://slack.com/api/chat.postMessage'

    payload = {
        "channel": "task-notifications",
        "text":f"Someone just completed the task {task.title}"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(api_url, headers=headers, data=payload)

    print(response.text)