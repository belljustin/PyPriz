from flask import redirect, session, url_for

def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
