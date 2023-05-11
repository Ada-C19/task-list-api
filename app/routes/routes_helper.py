from flask import abort, make_response
from app.models.task import Task 
def validate_model(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{cls.__name__} {id} invalid"}, 400))
    
    model = cls.query.get(id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))

    return model

def validate_data(cls, request_body):
    
    if "title" not in request_body or (cls == Task and "description" not in request_body):
        abort(make_response({"details": "Invalid data"}, 400))

    return request_body