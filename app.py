from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

import bcrypt
import os

app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    salt = db.Column(db.Binary(80))
    password = db.Column(db.Binary(80))
    score = db.Column(db.Integer)

    def __init__(self, username, email, salt, password):
        self.username = username
        self.email = email
        self.salt = salt
        self.password = password
        self.score = 0

    def __repr__(self):
        return '<User %r>' % self.username

def register(username, email, password):
    password = bytes(password, 'utf-8')
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return False
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    user = User(username, email, salt, hashed_password)
    db.session.add(user)
    db.session.commit()
    session['user'] = {'id': user.id, 'username': user.username}
    return True

def validate_login(email, password):
    password = bytes(password, 'utf-8')
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    if bcrypt.hashpw(password, user.salt) != user.password:
        return False
    session['user'] = {'id': user.id, 'username': user.username}
    return True

@app.route('/')
def index():
    user = None
    if 'user' in session:
        user = session['user']
    users = User.query.limit(10).all()
    return render_template('landing/landing.html', user=user, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'login' in request.form:
            if validate_login(request.form['email'], request.form['password']):
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='LOGIN_ERROR')

        elif 'register' in request.form:
            if register(request.form['username'], request.form['email'], request.form['password']):
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='REGISTER_ERROR')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    if not 'user' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        f = request.files['botfile']
        f.save(os.path.join(os.getcwd(), "bots", str(session['user']['id']) + '.py'))
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()
