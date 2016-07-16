DEBUG = True
# You can generate your own secret key with:
# $ python
# $ import os
# $ os.urandom(24)
SECRET_KEY = 'your_secret_key_here'

# database
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

