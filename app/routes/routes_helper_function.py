from flask import abort, make_response

def handle_valid_id(model, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({'Error':f'Invalid id "{task_id}"'}, 400))

    task = model.query.get(task_id)

    return task if task else abort(make_response(
        {'Error':f'No {model.__name__} with id {task_id}'}, 404
        ))    

