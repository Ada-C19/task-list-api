import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
text = "Someone just burnt the midnight oil"
# auth_header = {"Authorization": f"Bearer {token}"}

response = requests.post('https://slack.com/api/chat.postMessage', data={"token": token, "channel": "task-notifications", "text": text})
print(response.status_code)
print(response.json())



    # slack_response = requests.post('https://slack.com/api/chat.postMessage', data={"channel": "task-notifications", "text": text}, headers=auth_header)
    # print.response.status_code