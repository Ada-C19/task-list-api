from app import create_app, db
from app.models.task import Task

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="buy tomatoes", description="roma, organic", completed_at=None))
    db.session.add(Task(title="shopping toys for baby", description="montessori", completed_at=None))
    db.session.add(Task(title="trim the garden", description="buy fertilizer", completed_at=None))
    db.session.add(Task(title="buy cat sand", description="extra smell", completed_at=None))
    db.session.commit()