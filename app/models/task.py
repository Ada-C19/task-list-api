from app import db
from sqlalchemy.sql import false

### Task Model

# There should be a `Task` model that lives in `app/models/task.py`.

# Tasks should contain these attributes. Feel free to change the name of the `task_id` column if you would like. **The tests require the remaining columns to be named exactly** as `title`, `description`, and `completed_at`.

# - `task_id`: a primary key for each task
# - `title`: text to name the task
# - `description`: text to describe the task
# - `completed_at`: a datetime that has the date that a task is completed on. **Can be _nullable_,** and contain a null value. A task with a `null` value for `completed_at` has not been completed. When we create a new task, `completed_at` should be `null` AKA `None` in Python.

# ### Tips

# - SQLAlchemy's column type for text is `db.String`. The column type for datetime is `db.DateTime`.
# - SQLAlchemy supports _nullable_ columns with specific syntax.
# - Don't forget to run:
#   - `flask db init` once during setup
#   - `flask db migrate` every time there's a change in models, in order to generate migrations
#   - `flask db upgrade` to run all generated migrations
# - We can assume that the value of each task's `completed_at` attribute will be `None`, until wave 3. (Read below for examples)
# - We can assume that the API will designate `is_complete` as `false`, until wave 3. (Read below for examples)

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, server_default=None)
    is_complete = db.Column(db.Boolean, nullable=True, server_default=false())

