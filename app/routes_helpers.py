from flask import abort, make_response,request
import requests
from app import token

def validate_model(cls, model_id):
        try:
            model_id = int(model_id)
        except:
            abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

        model = cls.query.get(model_id)

        if not model:
            abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

        return model

def slack_call(task):
    path = "https://slack.com/api/chat.postMessage"

    data = {
            "channel": "U04M9CL7W6Q",
            "text": f"Someone just completed the task {task['title']}"
            }
    headers = {
                'Authorization': f'Bearer {token}',
                }

    response = requests.patch(path, data=data, headers=headers)

    return response.text

def query_sort(cls):
    sort_by = request.args.get('sort')
    title_param = request.args.get('title')

    if not title_param or not sort_by:
        cls_query = cls.query

    if title_param: 
            cls_query = cls.query.filter(cls.title.ilike(f'%{title_param}%'))
            
    if sort_by:
        if 'asc' in sort_by:
            if not 'id' in sort_by:
                cls_query = cls_query.order_by(cls.title.asc())
            else: cls_query = cls_query.order_by(cls.id.asc())
        elif 'desc' in sort_by:
            if not 'id' in sort_by:
                cls_query = cls_query.order_by(cls.title.desc())
            else: cls_query = cls_query.order_by(cls.id.desc())

    return cls_query

def to_dict(cls):
    cls_dict = dict(id=cls.id, title=cls.title)
    try:
        cls_dict['description'] = cls.description
        cls_dict['is_complete'] = cls.completed_at != None

        if cls.goal_id:
                cls_dict['goal_id'] = cls.goal_id
        
        return cls_dict
    
    except AttributeError:
        return cls_dict
