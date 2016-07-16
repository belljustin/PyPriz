from . import db

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(120), unique=True)
    token = db.Column(db.Binary(80))

    def __init__(self, ip_address, token):
        self.ip_address = ip_address
        self.token = token

    def __repr__(self):
        return '<Token %r>' % self.ip_address
