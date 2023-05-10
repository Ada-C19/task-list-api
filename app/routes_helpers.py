from flask import abort, make_response
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
                'Authorization': token,
                }

    response = requests.request("POST", path, headers=headers, data=data)

    return response.text
