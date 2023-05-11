from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title = task_data['title'],
            description = task_data['description']
        )
        
        return new_task
    
    def to_dict(self):
        return {
            'id':self.task_id,
            'title':self.title,
            'description':self.description,
            'is_complete': True if self.completed_at else False,
            # 'completed_at':self.completed_at   
        }
    
    def to_dict_one_task(self):
        return { 
                'task':
                self.to_dict()
                # {
                #     'id':self.task_id,
                #     'title':self.title,
                #     'description':self.description,
                #     'is_complete': True if self.completed_at else False

                                                     
                #     # 'completed_at':self.completed_at
                # }
        }
    
    