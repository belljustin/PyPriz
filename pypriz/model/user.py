from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120), unique=True)
    salt = db.Column(db.Binary(80))
    password = db.Column(db.Binary(80))

    def __init__(self, username, email, salt, password):
        self.username = username
        self.email = email
        self.salt = salt
        self.password

    def __repr__(self):
        return '<User %r>' % self.username
