import os

from flask import render_template, request, redirect, session, url_for

from settings import root

def upload():
    if not 'user' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            f = request.files['botfile']
            print(root)
            f.save(os.path.join(root, 'bots', str(session['user']['id']) + '.py'))
            return render_template('upload.html')
        except Exception as e:
            print(e)

