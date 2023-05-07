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


@tasks_bp.route("", methods=['POST'])
def create_task():
    new_task = get_task_instance(request)

    db.session.add(new_task)
    db.session.commit()

    # message = "201 CREATED"

    task = new_task.to_json()


    return make_response(jsonify(task=task), 201)






# ```json
# {
#   "task": {
#     "id": 1,
#     "title": "A Brand New Task",
#     "description": "Test Description",
#     "is_complete": false
#   }
# }
# ```

# so that I know I successfully created a Task that is saved in the database.

# ### Get Tasks: Getting Saved Tasks

# As a client, I want to be able to make a `GET` request to `/tasks` when there is at least one saved task and get this response:

# `200 OK`

# ```json
# [
#   {
#     "id": 1,
#     "title": "Example Task Title 1",
#     "description": "Example Task Description 1",
#     "is_complete": false
#   },
#   {
#     "id": 2,
#     "title": "Example Task Title 2",
#     "description": "Example Task Description 2",
#     "is_complete": false
#   }
# ]
# ```

# ### Get Tasks: No Saved Tasks

# As a client, I want to be able to make a `GET` request to `/tasks` when there are zero saved tasks and get this response:

# `200 OK`

# ```json
# []
# ```

# ### Get One Task: One Saved Task

# As a client, I want to be able to make a `GET` request to `/tasks/1` when there is at least one saved task and get this response:

# `200 OK`

# ```json
# {
#   "task": {
#     "id": 1,
#     "title": "Example Task Title 1",
#     "description": "Example Task Description 1",
#     "is_complete": false
#   }
# }
# ```

# ### Update Task

# As a client, I want to be able to make a `PUT` request to `/tasks/1` when there is at least one saved task with this request body:

# ```json
# {
#   "title": "Updated Task Title",
#   "description": "Updated Test Description",
# }
# ```

# and get this response:

# `200 OK`

# ```json
# {
#   "task": {
#     "id": 1,
#     "title": "Updated Task Title",
#     "description": "Updated Test Description",
#     "is_complete": false
#   }
# }
# ```

# Note that the update endpoint does update the `completed_at` attribute. This will be updated with custom endpoints implemented in Wave 03.

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