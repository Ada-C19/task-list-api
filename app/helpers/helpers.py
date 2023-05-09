from flask import abort, make_response


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} is invalid"
        abort(make_response({"message" : message}, 400))
    
    model = cls.query.get(model_id)
    
    if not model:
        message = f"{cls.__name__} {model_id} not found"
        abort(make_response({"message": message}, 404))
    
    return model