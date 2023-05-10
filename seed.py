from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="Fold laundry", description="chore"))
    db.session.add(Task(title="Wash dishes", description="chore"))
    db.session.add(Task(title="Work on task list", description="ada"))
    db.session.add(Task(title="Water plants", description="plant care"))
    db.session.commit()