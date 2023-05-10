from flask import abort, make_response

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"The {cls.__name__} #{model_id} is invalid"
        abort (make_response(f"Message: {message}", 400))

    model = cls.query.get(model_id)

    if not model:
        message = f"The {cls.__tablename__} #{model_id} not found"
        abort(make_response({"Message": message}, 404))

    return model