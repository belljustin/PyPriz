from pypriz.app import create_app
from pypriz.model import db

app = create_app('pypriz.settings')
db.init_app(app)
app.run()
