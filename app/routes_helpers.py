from flask import abort, make_response, jsonify
from app.models.task import Task


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": f"{cls.__name__} not found"}, 404))

    return model


def respond_with_json(data, status_code=200):
    response = jsonify(data)
    response.status_code = status_code
    return response
