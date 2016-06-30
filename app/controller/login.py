import bcrypt

from flask import render_template, request, redirect, session, url_for

from model import db
from model.user import User


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
