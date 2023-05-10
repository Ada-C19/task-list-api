from flask import abort, make_response

def validate_object(cls, object_id):
    # handle invalid object id, return 400
    try:
        object_id = int(object_id)
    except:
        abort(make_response({"msg": f"{cls.__name__} {object_id} is invalid."}, 400))

    obj = cls.query.get(object_id)
    if obj is None:
        abort(make_response({"msg": f"{cls.__name__} not found."}, 404))

    return obj