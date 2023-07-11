def notify_slack(token, task_name):
    import requests
    # import os
    # from dotenv import load_dotenv

    # load_dotenv()

    # token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
    text = f"Someone just completed {task_name}"
    # auth_header = {"Authorization": f"Bearer {token}"}

    slack_response = requests.post('https://slack.com/api/chat.postMessage', data={"token": token, "channel": "task-notifications", "text": text})
    # print(response.status_code)
    print(slack_response.json())
    
    return slack_response

# import os
# notify_slack(os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN"))


    # slack_response = requests.post('https://slack.com/api/chat.postMessage', data={"channel": "task-notifications", "text": text}, headers=auth_header)
    # print.response.status_code