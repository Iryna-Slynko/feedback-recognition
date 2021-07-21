from datetime import date
from server import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(32))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(64), unique=True)
    token = db.Column(db.String(128))
    token_start = db.Column(db.String(3))
    location_id = db.Column(db.Integer)

    def set_token(self, token):
        self.token =  generate_password_hash(token)
        self.token_start = token[0:3]

    def masked_token(self):
        return self.token_start + '*****'

    def __repr__(self):
        return '<Client {}>'.format(self.client)   


class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    upvote = db.Column(db.Boolean)
    created = db.Column(db.Date, index=True, default=date.today)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'))

    def __repr__(self):
        return '<Vote {}>'.format(self.vote_id)
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id'         : self.vote_id,
           'created'    : self.created.isoformat(),
           'upvote'     : self.upvote,
           'client_id'  : self.client_id
       }