from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def get_task_instance(request):
        task_info = request.get_json()
        return Task(
                title = task_info["title"],
                description = task_info["description"],
                completed_at = None
    )

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Invalid task ID: {task_id}"}, 400))

    return task_id

def get_task_by_id(task_id):
    task_id = validate_task_id(task_id)
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({'message': f'Task {task_id} was not found.'}, 404))
        
    return task 

def update_task_from_request(task, request):
    task_info = request.get_json()

    task.title = task_info["title"],
    task.description = task_info["description"],
    task.completed_at = None

    return task


@tasks_bp.route("", methods=['POST'])
def create_task():
    new_task = get_task_instance(request)

    db.session.add(new_task)
    db.session.commit()

    task = new_task.to_json()

    return make_response(jsonify(task=task)), 201

@tasks_bp.route("", methods=['GET'])
def get_tasks():
    tasks = Task.query.all()

    task_list = [task.to_json() for task in tasks]

    return jsonify(task_list), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = get_task_by_id(task_id)
    return make_response(jsonify({"task": task.to_json()})), 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    task = get_task_by_id(task_id)
    updated_task = update_task_from_request(task, request)

    db.session.commit()

    task = updated_task.to_json()

    return make_response(jsonify(task=task)), 200






# ### Delete Task: Deleting a Task

# As a client, I want to be able to make a `DELETE` request to `/tasks/1` when there is at least one saved task and get this response:

# `200 OK`

# ```json
# {
#   "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
# }
# ```

# ### No matching Task: Get, Update, and Delete

# As a client, if I make any of the following requests:

#   * `GET` `/tasks/<task_id>`
#   * `UPDATE` `/tasks/<task_id>`
#   * `DELETE` `/tasks/<task_id>`

# and there is no existing task with `task_id`

# The response code should be `404`.

# You may choose the response body.

# Make sure to complete the tests for non-existing tasks to check that the correct response body is returned.
 

# ### Create a Task: Invalid Task With Missing Data

# #### Missing `title`

# As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body

# ```json
# {
#   "description": "Test Description",
#   "completed_at": null
# }
# ```

# and get this response:

# `400 Bad Request`

# ```json
# {
#   "details": "Invalid data"
# }
# ```

# so that I know I did not create a Task that is saved in the database.

# #### Missing `description`

# If the HTTP request is missing `description`, we should also get this response:

# `400 Bad Request`

# ```json
# {
#   "details": "Invalid data"
# }
# ```

# #### Missing `completed_at`

# If the HTTP request is missing `completed_at`, we should also get this response:

# `400 Bad Request`

# ```json
# {
#   "details": "Invalid data"
# }
# ```

# __________