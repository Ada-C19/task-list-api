from flask import abort, make_response

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model


def create_model(cls, request_body):
    try:
        model = cls.from_dict(request_body)
    except KeyError:
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
