from app import User
from app import db

j = User.query.first()
User.query.delete()
db.session.commit()
