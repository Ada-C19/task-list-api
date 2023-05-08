from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import requests, os

task_list_bp = Blueprint("task_list_bp", __name__, url_prefix="/tasks")
goal_list_bp = Blueprint("goal_list_bp", __name__, url_prefix="/goals")


### Get Tasks: No Saved Tasks
### Get Tasks: Getting Saved Tasks
### Sorting Tasks: By Title, Ascending
### Sorting Tasks: By Title, Descending
@task_list_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []
    if len(tasks) != 0:
        sort_query = request.args.get("sort")
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
            
        else:
            tasks = Task.query.order_by(Task.title.desc())
            
        for task in tasks:
            tasks_response.append( {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete_status(task.completed_at)
                } )
        
    return jsonify(tasks_response)

### Create a Task: Valid Task With `null` `completed_at`
### Create a Task: Invalid Task With Missing Data
#### Missing `title`
#### Missing `description`
@task_list_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    
    db.session.add(new_task)
    db.session.commit()
    
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False    
    } }, 201
            
### Get One Task: One Saved Task
@task_list_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_item(Task, task_id)
    
    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_status(task.completed_at)
    } }
    
### Update Task
@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_item(Task, task_id)
    
    request_data = request.get_json()
    
    task.title = request_data["title"]
    task.description = request_data["description"]
    
    db.session.commit()
    
    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False    
    } }

### Delete Task: Deleting a Task
@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_item(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}

### Mark Complete on an Incompleted Task
### Mark Incomplete on a Completed Task
### Mark Complete on a Completed Task
### Mark Incomplete on an Incompleted Task
@task_list_bp.route("/<task_id>/<mark_status>", methods=["PATCH"])
def mark_comp_or_incomp(task_id, mark_status):
    task = validate_item(Task, task_id)
    # task is an instance that's being updated
    
    if mark_status == "mark_complete":
        task.completed_at = datetime.today()
        path = "https://slack.com/api/chat.postMessage"
        slack_api_token = os.environ.get("SLACK_API_TOKEN")

        response = requests.patch(path, data = {"channel": "task-notifications",
                                        "text": f"Someone just completed the task {task.title}"}, 
                                        headers = {"Authorization": f"Bearer {slack_api_token}"})
        # response is an object
                
    else:
        task.completed_at = None

    db.session.commit()
    
    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_status(task.completed_at)
    } } 
    
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
    
# Helper function
def is_complete_status(completed_at):
    if completed_at is None:
        return False
    else:
        return True
    
    
# Create new goal
@goal_list_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])
    
    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
        } }, 201
    
# Get all saved goals or zero saved goals
@goal_list_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    if len(goals) != 0:
        for goal in goals:
            goals_response.append( {
                "id": goal.goal_id,
                "title": goal.title
            } )
    return jsonify(goals_response)

# Get one goal
@goal_list_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title
    } }
    
# Update goal
@goal_list_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    request_data = request.get_json()
    
    goal.title = request_data["title"]
    
    db.session.commit()
    
    return {"goal": {
        "id": goal.goal_id,
        "title": goal.title
    }}
    
# Delete goal
@goal_list_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_item(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

    

    
    
    