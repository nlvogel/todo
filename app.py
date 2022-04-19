from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from private import secret_key, db_name


# initialize flask project
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
csrf = CSRFProtect(app)

#initialize db
app.config['SQLALCHEMY_DATABASE_URI'] = db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# set up alembic for database updates
migrate = Migrate(app, db)
