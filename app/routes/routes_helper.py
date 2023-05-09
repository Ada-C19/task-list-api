from flask import abort, make_response


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    
    task = Task.query.get(task_id)
    
    return task if task else abort(make_response({'msg': f"No task with id {task_id}"}, 404))

