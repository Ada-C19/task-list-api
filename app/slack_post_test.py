import requests
import time
import json

PATH = "https://slack.com/api/chat.postMessage"

Authorization = "Bearer xoxb-5242678399683-5266537240624-SzcfKHmF2xZaq407bmmGcsdL"

# seven_wonders = ["Great Wall of China","Petra", "Colosseum", "Chichen Itza", "Machu Picchu", "Taj Mahal", "Christ the Redeemer"]

headers = {
        "Authorization": Authorization,
        "format": "json"
    }

body = {
        "channel": "task-notifications",
        "text": "Hello, World!",
    }


requests.post(PATH, headers=headers, json=body)
# response_data = response.json()



# print("Response data:", response_data)
