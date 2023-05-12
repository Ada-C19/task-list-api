from flask import abort, make_response
import requests
from app import token


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} is invalid"
        abort(make_response({"message" : message}, 400))
    
    model = cls.query.get(model_id)
    
    if not model:
        message = f"{cls.__name__} {model_id} not found"
        abort(make_response({"message": message}, 404))
    
    return model

def send_message(task):

    url = "https://slack.com/api/chat.postMessage"

    request_body = {
        "channel" : "api-test-channel",
        "text" : f"Someone just completed the task {task.title}"
    }

    headers = {
        "Authorization" : f"Bearer {token}",
    }

    response = requests.post(url=url, headers=headers, data=request_body)
    
    print(response.text)