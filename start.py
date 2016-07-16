from pypriz.app import create_app
from pypriz.models import db

app = create_app('pypriz.settings')
db.init_app(app)
with app.app_context():
    db.create_all()
app.run()
