from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__,template_folder="templates")
app.secret_key='sdx2323@3343zbhcfew3rr3343@@###$2ffr454'
app.config.from_object(Config)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from views import *


