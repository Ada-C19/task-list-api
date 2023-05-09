from flask import jsonify, abort, make_response, request
from app import db


def validate_model(cls, id):
    try:
        id = int(id)
    except:
        message = f"{cls.__name__} {id} is invalid"
        abort(make_response({"message": message}, 400))

    model = cls.query.get(id)

    

    if not model:
        message = f"{cls.__name__} {id} not found"
        abort(make_response({"message": message}, 404))

    return model