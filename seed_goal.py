from app import create_app, db
from app.models.goal import Goal

my_app = create_app()
with my_app.app_context():
    db.session.add(Goal(title="be healthy"))
    db.session.add(Goal(title="raise better"))
    db.session.add(Goal(title="be happy"))
    db.session.add(Goal(title="continue being prosperous"))
    db.session.commit()