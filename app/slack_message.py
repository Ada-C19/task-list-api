import requests
from dotenv import load_dotenv
import os


load_dotenv()

path = "https://slack.com/api/chat.postMessage"

SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

def post_slack_message(task):
    request_body = {
        "channel" : "#api-test-channel",
        "text": f"Someone just completed the task {task.title}"
    }

    headers = {
        "Authorization" : SLACK_API_KEY
    }

    response = requests.post(path, data=request_body, headers=headers )
    response_body = response.json()
    return response_body




