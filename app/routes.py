from app import db
from app.models.task import Task 
from flask import Blueprint, make_response, abort, request, jsonify
from sqlalchemy.exc import DataError



bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#helper function
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)

    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model 


#routes

@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    missing_fields = []

    if "title" not in request_body:
        missing_fields.append("title")
    if "description" not in request_body:
        missing_fields.append("description")

    if missing_fields:
        error_dict = {
            "details": "Invalid data"
        }
        abort(make_response(jsonify(error_dict), 400))

    try:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()

        task_dict = new_task.to_dict()
        task_dict["is_complete"] = False

        response_body = {"task": task_dict}

        return make_response(jsonify(response_body)), 201
    
    except DataError as e:
        db.session.rollback()

        message = "Invalid request body: DataError"
        error_dict = {"message": message, "error": str(e)}
        abort(make_response(jsonify(error_dict), 400))