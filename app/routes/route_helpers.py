from flask import abort, make_response


def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response(
            {"details": f"{cls.__name__}  number {id} not valid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response(
            {"details": f"{cls.__name__} number {id} was not found"}, 404))

    return model
