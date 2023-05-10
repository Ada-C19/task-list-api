from app import db


class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    
    def to_dict(self):
        return {
                'id': self.id,
                'title': self.title
        }

    @classmethod
    def from_dict(cls, request_body):
        goal = cls(
                    title=request_body['title']
                    )
        return goal
        
    #returns all the attributes that must be passed in order to create a record. All not nullable instance variables accept id.'
    @classmethod
    def get_attributes(cls):
        return ['title']