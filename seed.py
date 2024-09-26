from datetime import datetime
from app import create_app, db
from app.models.task import Task
from app.models.goal import Goal

my_app = create_app()

with my_app.app_context():
    db.session.add(Task(title = "A New Task", description = "New", completed_at = None)) 
    db.session.add(Task(title = "A Newer Task", description = "Newer", completed_at = datetime.now())) 
    db.session.add(Task(title = "A Cool Task", description = "Cool", completed_at = None)) 
    db.session.add(Task(title = "A Cooler Task", description = "Cooler", completed_at = datetime(2022, 10, 8))) 
    db.session.add(Task(title = "A Neat Task", description = "Neat", completed_at = None)) 
    db.session.add(Task(title = "An Awesome Task", description = "Awesome", completed_at = datetime(2023, 2, 11))) 
    db.session.add(Task(title = "An Uncreative Task", description = "Uncreative", completed_at = None)) 
    db.session.add(Task(title = "An Old Task", description = "Old", completed_at = datetime(2023, 2, 10))) 
    db.session.add(Task(title = "A Tired Task", description = "Tired", completed_at = None)) 
    db.session.add(Task(title = "An Older Task", description = "Older", completed_at = datetime(2023, 1, 20))) 

    db.session.add(Goal(title = "Do Something")) 
    db.session.add(Goal(title = "Do Something Else")) 
    db.session.add(Goal(title = "Do Something More")) 
    db.session.add(Goal(title = "Do Something New")) 
    db.session.add(Goal(title = "Do Nothing")) 
    
    db.session.commit()