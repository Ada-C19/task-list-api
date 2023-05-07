from app import db

class Goal(db.Model):

    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # name = db.Column(db.String, nullable=False)
    # description = db.Column(db.String, nullable=False)
    # mass = db.Column(db.Numeric(precision=16, scale=3), nullable=False)

    # def to_dict(self):
    #         return {
    #         'id': self.id,
    #         'name': self.name,
    #         'description': self.description,
    #         'mass': self.mass,
    #         }
    