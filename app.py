from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


# initialize flask project
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["secret_key"]
csrf = CSRFProtect(app)

#initialize db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["db_name"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# set up alembic for database updates
migrate = Migrate(app, db)
