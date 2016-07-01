from flask import render_template, session
from flask.views import View

from model.user import User


class IndexView(View):
    def dispatch_request(self):
        user = None
        if 'user' in session:
            user = session['user']
        users = User.query.limit(10).all()
        return render_template('landing/landing.html', user=user, users=users)
