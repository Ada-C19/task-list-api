from flask import abort, make_response
from datetime import datetime

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
    
    if "title" not in request_body or (cls.__name__ == "Task" and "description" not in request_body):
        abort(make_response({"details": "Invalid data"}, 400))
    
    if "completed_at" in request_body:
        #format = "%Y-%m-%d-%H-%M-%S"
        format = "%Y-%m-%dT%H::%M::%S.%f"
        try:
            request_body["completed_at"]= datetime.strptime(request_body["completed_at"], format)
        except:
            abort(make_response({"message": f"{request_body['completed_at']} is not a valid date time"}, 400))

    return request_body

