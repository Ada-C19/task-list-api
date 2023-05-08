from flask import abort, make_response

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} with id {id} was not found."}, 404))

    return model 

def validate_req(cls, req_body):
    for i in cls().show_required():
        if i not in req_body:
            abort(make_response({"details": "Invalid data"}, 400))
