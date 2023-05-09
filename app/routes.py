from flask import Blueprint,make_response,request,jsonify,abort
from app import db
from app.models.task import Task

#CREATE BP/ENDPOINT
tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Task {id} is invalid"},400))

    task =  Task.query.get(id)

    if not task:
        abort(make_response({"message":f"Task {id} not found."},404))
    
    return task


#ROUTE FUNCTIONS
@tasks_bp.route("/<id>",methods=["GET"])
def read_one_task(id):
    task = validate_task(id)

    return jsonify(task.make_dict()),200


@tasks_bp.route("",methods=["POST"])
def create_a_task():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return make_response("Invalid Request",400)
        
        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return make_response(f"Task {new_task.title} successfully created",201)