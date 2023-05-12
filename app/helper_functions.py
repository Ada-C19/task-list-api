from flask import abort, make_response, request, jsonify
import requests
from dotenv import load_dotenv
import os
load_dotenv()

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def slack_mark_complete(self):
        API_KEY= os.environ.get("API_KEY")
        url = "https://slack.com/api/chat.postMessage"

        data = {
        "channel": "#task-list-api",
        "text": f"Someone just completed the task {self.title}"
        }
        headers = {
    'Authorization': f'{API_KEY}'
        }

        response = requests.post(url, headers=headers, data=data)

        print(response.text)