import os

# self application position(filesystem path)
basedir = os.path.abspath(os.path.dirname(__file__))

# DATABASE name and position
DATABASE = 'flasktask.db'
DATABASE_PATH = os.path.join(basedir, DATABASE)

# session management
SECRET_KEY = 'myprecious'

# security
WTF_CSRF_ENABLE = True

# temp user account
USERNAME = 'admin'
PASSWORD = 'admin'

