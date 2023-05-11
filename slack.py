# /task-list-api/app/slack.py
import os
import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_API_KEY")

def send_slack_notification(task_title):
    url = "https://slack.com/api/chat.postMessage"
    channel = "#task-notifications"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }

    data = {
    "channel": channel,
    "text": f"Task *{task_title}* has been marked as complete :white_check_mark:",
}



    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
