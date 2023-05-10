from flask import Blueprint, make_response, jsonify, request, abort
from app.models.task import Task
from app import db
from datetime import datetime
import requests
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

# client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
# logger = logging.getLogger(__name__)

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# def validate_request_body(request): finish later 



@bp.route("", methods=["GET"])
def get_all_tasks():
    # tasks = Task.query.all()


    sorted_query = request.args.get("sort")
    if sorted_query == "asc":
        tasks = Task.query.order_by("title")
    elif sorted_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    # name_query = request.args.get("name")
    # if name_query is None:
    #     planets = Planet.query.filter_by(name=name_query)
    # else:
    #     planets = Planet.query.all()


    tasks_list = []
    for task in tasks:
        tasks_list.append(task.to_dict()) 
        # tasks_list.append(task)
        
        # tasks_list.append(f"{
        #   "id:" {task.id}","
        #   "title:" {task.title}","
        #    "description:" {task.description}",
        #      "completed_at:" {task.completed_at}
        #    }")
        # tasks_list.append({
        #     "id": task.id,
        #     "title": task.title,
        #     "description": task.description,
        #     "completed_at": task.completed_at
        # })
    
    return jsonify(tasks_list), 200


@bp.route("", methods=["POST"])
def create_task():
    request_body=request.get_json()
    
    if "title" not in request_body or not request_body["title"] or "description" not in request_body or not request_body["description"]:
        abort(make_response({"details": "Invalid data"}, 400))
    else:

        # is_complete = request_body.get("is_complete", False) #find a way to include this in model class
        # if "completed_at" not in request_body or not request_body["completed_at"]:
        #     # request_body["is_complete"] = True
        #     is_complete = False
        # else:
        #     # request_body["is_complete"] = False
        #     is_complete = True



        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
            # is_complete=is_complete '''this commented out made it work
        )

        # new_task = Task.from_dict(request_body)
        
        db.session.add(new_task)
        db.session.commit()
        
        return {"task": new_task.to_dict()}, 201



def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response(f"Task number {id} not valid", 400))
    
    task = Task.query.get(id)

    if not task:
        abort(make_response(f"Task number {id} was not found", 404))
    
    return task



@bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)
    return {"task": task.to_dict()}, 200


@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    is_complete = request_body.get("is_complete", False)

    # is_complete = request_body.get("is_complete", False)

    # if request_body["is_complete"] == None:
    #     request_body["is_complete"] = False

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = is_complete 

    db.session.commit()

    return {"task": task.to_dict()}, 200

@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    return {"details" : f'Task {id} "{task.title}" successfully deleted'}, 200


@bp.route("/<id>/mark_complete", methods=["PATCH"])
def complete_task(id):
    task = validate_task(id)
    # request_body = request.get_json()

    # if request_body is None:
    #     return {"details": "Invalid data"}, 400

    # if "completed_at" in request_body:
    if not task.completed_at:
        task.completed_at = datetime.now()
    task.is_complete = True
    # else:
    #     return {"details": "Invalid data"}, 400

    PATH = "https://slack.com/api/chat.postMessage"

    Authorization = "Bearer xoxb-5242678399683-5266537240624-SzcfKHmF2xZaq407bmmGcsdL"

    headers = {
        "Authorization": Authorization,
        "format": "json"
    }

    body = {
        "channel": "task-notifications",
        "text": "Hello, World!",
    }
    requests.post(PATH, headers=headers, json=body)
    # response = requests.post(PATH, headers=headers, json=body)


    # # return response.json()
    # response_data = response.json()
    # print("Response data:", response_data)

    #channel_id = "C12345"

    # try:
    # # Call the chat.postMessage method using the WebClient
    #     result = client.chat_postMessage(
    #     channel=channel_id, 
    #     text="Hello world"
    # )
    #     logger.info(result)

    # except SlackApiError as e:
    # logger.error(f"Error posting message: {e}")

    db.session.commit()
    return {"task": task.to_dict()}, 200    


@bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(id):
    task = validate_task(id)
    # request_body = request.get_json()

    if task.completed_at:
        task.completed_at = None
    task.is_complete = False

    db.session.commit()
    return {"task": task.to_dict()}, 200




