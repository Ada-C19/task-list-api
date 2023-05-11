from flask import abort, make_response, request, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import timezone, datetime
from http import HTTPStatus


def validate_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        error_message = generate_error_message(cls, model_id)
        abort(make_response(error_message, HTTPStatus.BAD_REQUEST))
    return model_id


def get_model_by_id(cls, model_id):
    model_id = validate_id(cls, model_id)
    model = db.session.get(cls, model_id)

    if not model:
        error_message = generate_error_message(cls, model_id)
        abort(make_response(error_message, HTTPStatus.NOT_FOUND))  
        
    return model

def generate_error_message(cls, model_id):
    return {"message": f"{cls.__name__} {model_id} was not found."}


def create_instance(cls):
    instance_info = request.get_json()

    try:
        instance = cls.from_json(instance_info)
    except KeyError as err:
        abort(make_response({"details": f"KeyError invalid {cls.__name__} data, missing key: {err}"}, HTTPStatus.BAD_REQUEST))

    db.session.add(instance)
    db.session.commit()

    instance = instance.to_json()
    cls_type = cls.__name__.lower()

    return make_response(jsonify({cls_type: instance}), HTTPStatus.CREATED)


def get_all_instances(cls):
    instances = cls.query.all()

    instance_list = [instance.to_json() for instance in instances]

    return make_response(jsonify(instance_list), HTTPStatus.OK)


def get_one_instance(cls, model_id):
    instance = get_model_by_id(cls, model_id)
    
    instance = instance.to_json()
    cls_type = cls.__name__.lower()
    
    return make_response(jsonify({cls_type: instance}), HTTPStatus.OK)


def update_instance(cls, model_id):
    instance = get_model_by_id(cls, model_id)
    instance_info = request.get_json()

    if 'title' in instance_info:
        instance.title = instance_info['title']

    if cls is Task:
        if 'description' in instance_info:
            instance.description = instance_info['description']
        elif 'completed_at' in instance_info:
            instance.completed_at = instance_info['completed_at']
        else:
            instance.completed_at = None

    db.session.commit()

    instance = instance.to_json()
    cls_type = cls.__name__.lower()
    
    return make_response(jsonify({cls_type: instance}), HTTPStatus.OK)


def delete_instance(cls, model_id):
    instance = get_model_by_id(cls, model_id)

    db.session.delete(instance)
    db.session.commit()

    message = f'{cls.__name__} {model_id} "{instance.title}" successfully deleted'

    return make_response({"details" : message}, HTTPStatus.OK)

