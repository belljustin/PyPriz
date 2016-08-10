import bcrypt

from flask import render_template, request, redirect, session, url_for
from flask.views import View

from pypriz.models import db
from pypriz.models.user import User


class LoginView(View):
    def dispatch_request(self):
        if request.method == 'POST':
            return self.login(request.form['email'], request.form['password'])
        error = session.pop('error', None)
        return render_template('login.html', error=error)

    def login(self, email, password):
        if self.validate_login(email, password):
            return redirect(url_for('index'))
        return render_template('login.html', error='LOGIN_ERROR')

    def validate_login(self, email, password):
        password = bytes(password, 'utf-8')
        user = User.query.filter_by(email=email).first()
        if not user:
            return False
        if bcrypt.hashpw(password, user.salt) != user.password:
            return False
        session['user'] = {'id': user.id, 'username': user.username}
        return True


class RegisterView(View):
    def dispatch_request(self):
        return self.register(
            request.form['username'],
            request.form['email'],
            request.form['password'])

    def register(self, username, email, password):
        if self.validate_registration(username, email, password):
            return redirect(url_for('index'))
        session['error'] = 'REGISTRATION_ERROR'
        return redirect(url_for('login'))

    def validate_registration(self, username, email, password):
        password = bytes(password, 'utf-8')
        if User.query.filter_by(username=username).first() \
           or User.query.filter_by(email=email).first():
            return False
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        user = User(username, email, salt, hashed_password)
        print(user.password)
        db.session.add(user)
        db.session.commit()
        session['user'] = {'id': user.id, 'username': user.username}
        return True


class LogoutView(View):
    def dispatch_request(self):
        session.pop('user', None)
        return redirect(url_for('index'))
