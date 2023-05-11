from app import create_app, db
from app.models.task import Task
from app.models.goal import Goal

my_app = create_app()
with my_app.app_context():
    db.session.query(Task).delete()
    db.session.commit()

    db.session.add(Task(title="Fold laundry", description="chore"))
    db.session.add(Task(title="Wash dishes", description="chore"))
    db.session.add(Task(title="Work on task list", description="ada"))
    db.session.add(Task(title="Water plants", description="plant care"))

    db.session.add(Goal(title="Finish chores by end of the week"))
    db.session.add(Goal(title="Complete Ada project and work on optional enhancements"))
    db.session.commit()