import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("THE_SLACK_TOKEN")
text = "still got it"

slack_response = requests.post('https://slack.com/api/chat.postMessage', data={"token": token, "channel": "task-notifications", "text": text})
print(slack_response.status_code)
print(slack_response.json())



    # slack_response = requests.post('https://slack.com/api/chat.postMessage', data={"channel": "task-notifications", "text": text}, headers=auth_header)
    # print.response.status_code