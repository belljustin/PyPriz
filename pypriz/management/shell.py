from pypriz.app import create_app
from pypriz.model import db
from pypriz.model.user import User

app = create_app('pypriz.settings')
db.init_app(app)
