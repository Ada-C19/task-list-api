from flask import Blueprint, jsonify, make_response, abort, request, render_template, redirect, url_for
from app import db
from app.models.task import Task
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks", template_folder="templates")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return task

########## POST ########################################
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({'details': 'Invalid data'}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task.to_dict()}), 201

########### PUT #############################################
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    return jsonify({'task': task.to_dict()}), 200

############# PATCH ########################
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def patch_task_complete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.today()
    
    channel_id = 'task-notifications'
    url_endpoint = 'https://slack.com/api/chat.postMessage'
    params = {'channel': channel_id, 'text': f"Someone just completed the task {task.title}"}
    headers = {'Authorization': f"Bearer {os.environ.get('SLACK_API_KEY')}"}
    
    requests.post(url=url_endpoint, params=params, headers=headers)

    db.session.commit()
    return jsonify({'task': task.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def patch_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
    
    db.session.commit()
    return jsonify({'task': task.to_dict()}), 200

######### GET ###############################################
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({'task': task.to_dict()}), 200

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    task_query = request.args.get("sort")
    if task_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif task_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

####### DELETE #############################
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

######## UI ROUTES #######################
# @tasks_bp.route("/ui", methods=["GET", "POST"])
# def ui_route():
#     if request.method == 'POST':
#         task_title = request.form['title']
#         task_description = request.form['description']
#         new_task = Task(title=task_title, description=task_description)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an error while adding the task'

#     else:
#         tasks = Task.query.all()
#         return render_template("index.html", tasks=tasks)
    
# @tasks_bp.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Task.query.get_or_404(id)
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/ui')
#     except:
#         return 'There was an error while deleting that task'
    
# @tasks_bp.route('/update/<int:id>', methods=['GET','POST'])
# def update(id):
#     task = Task.query.get_or_404(id)

#     if request.method == 'POST':
#         task.title = request.form['title']
#         task.description = request.form['description']

#         try:
#             db.session.commit()
#             return redirect('/ui')
#         except:
#             return 'There was an issue while updating that task'

#     else:
#         return render_template('update.html', task=task)

@tasks_bp.route('/ui/')
def index():
    incomplete = Task.query.all()
    # complete = Task.query.filter_by(completed_at=True).all()
    return render_template('index.html', incomplete=incomplete)
                        # , complete=complete)

@tasks_bp.route('/ui/add', methods=['POST'])
def add():
    todo = Task(name=request.form['todoitem'], description="Test", completed_at=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@tasks_bp.route('/test/')
def test_page():
        return render_template('test.html')
