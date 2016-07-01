import os

from flask import render_template, request, redirect, session, url_for
from flask.views import View

from settings import BOT_FOLDER

class UploadView(View):
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def dispatch_request(self):
        if not 'user' in session:
            return redirect(url_for('index'))
        if request.method == 'POST':
            filename = "%d.py" % session['user']['id']
            f = request.files['botfile']
            f.save(os.path.join(self.upload_folder, filename))
            return render_template('upload.html')

