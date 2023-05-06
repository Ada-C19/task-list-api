from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="clean fridge", description="throw out the starter"))
    db.session.add(Task(title="Skype parents", description="Do some homework first"))
    db.session.add(Task(title="rearrange cabinets", description="Move glasses back into kitchen"))

    db.session.commit()
