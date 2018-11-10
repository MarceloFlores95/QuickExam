from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

Debug = os.environ.get('DEBUG', default='True')
if Debug.lower() in ('f', 'false'):
    Debug = False
else:
    Debug = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///QuickExam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER_UI_JSONEDITOR'] = True
app.config['SECRET_KEY'] = 'RuloEsHermoso' if Debug else os.urandom(16)
CORS(app)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(app, doc='/api/documentation', authorizations=authorizations)
db = SQLAlchemy(app)

from .models import *
from .resources import *

migrate = Migrate(app, db)
