from pypriz.app import create_app
from pypriz.models import db
from pypriz.models.user import User

app = create_app('pypriz.settings')
db.init_app(app)
