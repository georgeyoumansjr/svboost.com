# http://flask.pocoo.org/docs/1.0/tutorial/database/
import sqlite3
import io
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()