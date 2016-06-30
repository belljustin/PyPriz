from flask import render_template, session

from model.user import User

def index():
    user = None
    if 'user' in session:
        user = session['user']
    users = User.query.limit(10).all()
    return render_template('landing/landing.html', user=user, users=users)
