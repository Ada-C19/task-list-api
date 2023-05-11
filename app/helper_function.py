
from flask import abort, make_response

def get_valid_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'message': f"Invalid {model.__name__} '{id}'"}, 400))

    item = model.query.get(id)

    return item if item else abort(make_response({'message': f"No {model.__name__} with id {id}"}, 404))