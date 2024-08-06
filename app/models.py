from . import db
from flask_login import UserMixin
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    initial_case = db.Column(db.Integer, nullable=True)
    cases = db.Column(db.String, nullable=False, default=json.dumps([i for i in range(1, 27)]))
    revealed_cases = db.Column(db.String, nullable=False, default=json.dumps([]))
    offers = db.Column(db.String, nullable=False, default=json.dumps([]))
    final_offer = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'initial_case': self.initial_case,
            'cases': json.loads(self.cases),
            'revealed_cases': json.loads(self.revealed_cases),
            'offers': json.loads(self.offers),
            'final_offer': self.final_offer,
        }
