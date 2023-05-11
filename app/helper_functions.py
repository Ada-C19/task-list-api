import requests

def slack_mark_complete(self):
        url = "https://slack.com/api/chat.postMessage"

        data = {
        "channel": "#task-list-api",
        "text": f"Someone just completed the task {self.title}"
        }
        headers = {
    'Authorization': 'Bearer xoxb-5245529664147-5239168009126-Tl7hTy4y6CCqqpi9jP6BJuVv'
        }

        response = requests.post(url, headers=headers, data=data)

        print(response.text)