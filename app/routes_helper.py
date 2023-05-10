from flask import abort, make_response
"""
    A route helper function that return queried item by valid id;
    or return message and 404 response for invalid id.
"""
def validate_item_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid id '{id}'"}, 400))
    item = model.query.get(id)
    return item if item else abort(make_response({'msg': f"No {model.__name__} with id {id}"}, 404))