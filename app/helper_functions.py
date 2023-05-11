def validate_model(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))
    
    return task

def slack_bot_message(message):
    slack_api_key = os.environ.get("SLACK_BOT_TOKEN")
    slack_url = "https://slack.com/api/chat.postMessage"
    header = {"Authorization": slack_api_key}

    slack_query_params = {
        "channel": "task-notifications",
        "text": message
    }
    print(slack_api_key)
    requests.post(url=slack_url, data=slack_query_params, headers=header)