import os

from flask import render_template, request, redirect, session, url_for

from settings import settings

def upload():
    if not 'user' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        f = request.files['botfile']
        f.save(settings['BOT_FOLDER'])
        return render_template('upload.html')

