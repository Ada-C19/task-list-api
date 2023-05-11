from flask import make_response, abort


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        message = {"message": f"Invalid {cls.__name__} id {model_id}"}
        abort(make_response(message, 400))

    model = cls.query.get(model_id)

    if not model:
        message = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(message, 404))
    else:
        return model
