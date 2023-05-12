from flask import make_response, request, jsonify, abort
from app import db
from http import HTTPStatus
from sqlalchemy import asc, desc
from datetime import timezone, datetime
from dotenv import load_dotenv

load_dotenv()

NOWTIME = datetime.now(timezone.utc)
# SLACK_TOKEN = os.environ.get("SLACK_TOKEN")




def create_response(cls, instance, status_code=HTTPStatus.OK):
    db.session.commit()
    instance = instance.to_json()
    cls_type = cls.__name__.lower()
    return make_response(jsonify({cls_type: instance}), status_code)


def generate_error_message(cls, id):
    return {"message": f"{cls.__name__} {id} was not found."}






def validate_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message = generate_error_message(cls, id)
        return error_response(error_message, HTTPStatus.BAD_REQUEST)
    return id

def validate_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message = generate_error_message(cls, id)
        abort(make_response(error_message, HTTPStatus.BAD_REQUEST))
    return id


def get_model_by_id(cls, id):
    id = validate_id(cls, id)
    model = db.session.get(cls, id)

    if not model:
        error_message = generate_error_message(cls, id)
        abort(make_response(error_message, HTTPStatus.NOT_FOUND))

    return model


def create_instance(cls):
    instance_info = request.get_json()

    try:
        instance = cls.from_json(instance_info)
    except KeyError as err:
        error_message = {"details": f"KeyError invalid {cls.__name__} data, missing key: {err}"}
        return make_response(jsonify(error_message), HTTPStatus.BAD_REQUEST)

    db.session.add(instance)

    return create_response(cls, instance, HTTPStatus.CREATED)


def get_all_instances(cls):
    sort_order = request.args.get("sort")

    instances = cls.query

    title_query = request.args.get("title")
    if title_query:
        instances = instances.filter_by(title=title_query)

    if sort_order == "asc":
        instances = instances.order_by(asc(cls.title))
    elif sort_order == "desc":
        instances = instances.order_by(desc(cls.title))

    if hasattr(cls, 'description'):
        if sort_order == "description_asc":
            instances = instances.order_by(asc(cls.description))
        elif sort_order == "description_desc":
            instances = instances.order_by(desc(cls.description))

    instance_list = [instance.to_json() for instance in instances]

    return make_response(jsonify(instance_list), HTTPStatus.OK)


def get_one_instance(cls, id):
    instance = get_model_by_id(cls, id)
    return create_response(cls, instance, HTTPStatus.OK)


def update_instance(cls, id):
    instance = get_model_by_id(cls, id)
    instance_info = request.get_json()

    if 'title' in instance_info:
        instance.title = instance_info['title']

    if hasattr(cls, 'description'):
        if 'description' in instance_info:
            instance.description = instance_info['description']
        elif 'completed_at' in instance_info:
            instance.completed_at = instance_info['completed_at']
        else:
            instance.completed_at = None

    return create_response(cls, instance)


def delete_instance(cls, id):
    instance = get_model_by_id(cls, id)

    db.session.delete(instance)
    db.session.commit()

    message = f'{cls.__name__} {id} "{instance.title}" successfully deleted'

    return make_response({"details": message}, HTTPStatus.OK)


def make_instance_complete(cls, id):
    instance = get_model_by_id(cls, id)

    instance.completed_at = NOWTIME

    return create_response(cls, instance)


def make_instance_incomplete(cls, id):
    instance = get_model_by_id(cls, id)

    instance.completed_at = None

    return create_response(cls, instance)

