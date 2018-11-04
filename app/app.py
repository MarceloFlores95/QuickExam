from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///QuickExam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER_UI_JSONEDITOR'] = True
CORS(app)
api = Api(app, doc='/api/documentation')
db = SQLAlchemy(app)

from .models import *
from .resources import *

migrate = Migrate(app, db)
