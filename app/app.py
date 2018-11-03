from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///QuickExam.db'
api = Api(app)
db = SQLAlchemy(app)

from .models import *

migrate = Migrate(app, db)
