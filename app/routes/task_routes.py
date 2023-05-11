from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import requests, os

task_list_bp = Blueprint("task_list_bp", __name__, url_prefix="/tasks")

### Get Tasks: No Saved Tasks
### Get Tasks: All Saved Tasks
### Sorting Tasks: By Title, Ascending
### Sorting Tasks: By Title, Descending
@task_list_bp.route("", methods=["GET"])
def get_tasks():
    # get all tasks 
    tasks = Task.query.all()
    # initialize list of tasks
    tasks_response = []
    # get sort param value if tasks exist
    if len(tasks) != 0:
        sort_query = request.args.get("sort")
        # sort tasks ascending if sort is asc
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        
        # sort tasks descending if sort is desc   
        else:
            tasks = Task.query.order_by(Task.title.desc())
        
        # loop thru each task      
        for task in tasks:
            # return task dict and add it to list
            tasks_response.append(task.to_dict())
    
    # return list of task dicts    
    return jsonify(tasks_response)

### Create a Task: Valid Task With `null` `completed_at`
### Create a Task: Invalid Task With Missing Data
#### Missing `title`
#### Missing `description`
@task_list_bp.route("", methods=["POST"])
def create_task():
    # get request data
    request_body = request.get_json()
    # if title or description doesn't exist in request data, return 400 mesg
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    
    # create new task from request data
    new_task = Task.from_dict(request_body)
    
    # add and commit new task
    db.session.add(new_task)
    db.session.commit()
    
    # return dict of task dicts
    return {"task": new_task.to_dict()}, 201
            
### Get One Task
@task_list_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    # return task if task_id valid and exists
    task = validate_item(Task, task_id)
    
    # if goal doesn't exist, return task dict
    if task.goal is None:
            return {"task": task.to_dict() }
    else:
        # otherwise, return add goal_id:value pair and return
        # dict of task dicts
        task_with_goal = task.to_dict()
        task_with_goal["goal_id"] = task.goal_id
        return {"task": task_with_goal}
    
### Update Task
@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    # return task if task_id valid and exists
    task = validate_item(Task, task_id)
    
    # get request data
    request_data = request.get_json()
    
    # update task title and description from request data
    task.title = request_data["title"]
    task.description = request_data["description"]
    
    # commit updated task
    db.session.commit()
    
    # return dict of task dicts
    return {"task": task.to_dict()}

### Delete Task
@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # return task if task_id valid and exists
    task = validate_item(Task, task_id)
    
    # delete task and commit delete
    db.session.delete(task)
    db.session.commit()
    
    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}

### Mark Complete on an Incompleted Task
### Mark Incomplete on a Completed Task
### Mark Complete on a Completed Task
### Mark Incomplete on an Incompleted Task
@task_list_bp.route("/<task_id>/<mark_status>", methods=["PATCH"])
def mark_comp_or_incomp(task_id, mark_status):
    # return task if task_id valid and exists
    task = validate_item(Task, task_id)
    # task is an instance that's being updated
    
    # if mark_complete, update completed_at w/ today's datetime and call Slack API
    if mark_status == "mark_complete":
        task.completed_at = datetime.today()
        path = "https://slack.com/api/chat.postMessage"
        slack_api_token = os.environ.get("SLACK_API_TOKEN")

        requests.patch(path, data = {"channel": "task-notifications",
                                        "text": f"Someone just completed the task {task.title}"}, 
                                        headers = {"Authorization": f"Bearer {slack_api_token}"})
        # above is an object

    # otherwise, leave completed_at as null            
    else:
        task.completed_at = None

    # commit changes
    db.session.commit()
    
    # return dict of task dicts
    return {"task": task.to_dict()} 
    
### No matching Task or Goal: Get, Update, and Delete
## Mark Complete and Mark Incomplete for Missing Tasks
# Helper function
def validate_item (model, item_id):
    try:
        item_id_int = int(item_id)
    except:
        return abort(make_response({"message":f"Item {item_id} invalid"}, 400))
    
    item = model.query.get(item_id_int)
    
    if not item:
        return abort(make_response({"message":f"Item {item_id_int} not found"}, 404))
    
    return item    
    

    

    

    
    
    