from flask import jsonify, abort, make_response

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response(jsonify(f"{cls.__name__} {id} is invalid"), 400))
    model = cls.query.get(id)
    if not model:
        abort(make_response(jsonify(f"{cls.__name__} {id} not found"), 404))
    return model