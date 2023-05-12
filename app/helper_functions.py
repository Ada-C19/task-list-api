from flask import abort, make_response
from datetime import datetime

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model


def update_model(model, request_body):
    if "completed_at" in request_body:
        try:
            request_body["completed_at"] = datetime(request_body["completed_at"])
        except TypeError:
            abort(make_response({"details": "Invalid data"}, 400))
    for attribute, value in request_body.items():
        try:
            setattr(model, attribute, value)
            # setattr() is a built-in Python function that sets the value of 
            # a named attribute of an object. It takes 3 arguments: the object to modify,
            # the name of the attribute to set, and the value to set 
        except KeyError:
            return abort(make_response({"details": "Invalid data"}, 400))


def create_model(cls, request_body):
    try:
        model = cls.from_dict(request_body)
    except (KeyError, TypeError):
        return abort(make_response({"details": "Invalid data"}, 400))
    return model


def sort_items(items, sort_query):
    if sort_query == "desc":
        models = items.query.order_by(items.title.desc()).all()
    elif sort_query == "asc":
        models = items.query.order_by(items.title.asc()).all()
    else: # sort items by id in ascending order by default
        models = items.query.order_by(items.id.asc()).all()
    return models 
