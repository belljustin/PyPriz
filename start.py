from pypriz.app import create_app
from pypriz.model import db

app = create_app('pypriz.settings')
with app.app_context():
    db.init_app(app)
app.run()
