from flask import abort, make_response
from dotenv import load_dotenv
import requests
import os


def validate_id(model, id):
    if not id.isnumeric():
        abort(make_response({'Error': f'{id} is invalid'}, 400))
    
    entity = model.query.get(id)
    if not entity:
        abort(make_response({'Not found': f'No {model.__name__} with id#{id} is found'}, 404))
    return entity

def validate_entry(model, request_body):
    for atr in model.get_attributes():
        if atr not in request_body:
            abort(make_response({'details': 'Invalid data'}, 400))
            # abort(make_response({'Invalid Request': f'Missing {model.__name__} {atr}'}, 400))
    return request_body

def slack_notification(entity):
    slack_url = 'https://slack.com/api/chat.postMessage'
    token = os.environ.get("SLACK_API_TOKEN")
    notification = {'channel': 'task-notifications', 'text': f'Yeaaaay! Tha task {entity.title} is now completed! Congrats :-)'}
    headers = {'Content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    requests.post(slack_url, json=notification, headers=headers)