from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    
    def to_dict(self):
        task_dict = {}
        task_dict['id'] = self.task_id
        task_dict['title'] = self.title
        task_dict['description'] = self.description
        task_dict['is_complete'] = False
        
        return task_dict