from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    }
}

db = SQLAlchemy()
api = Api( doc='/api/documentation', authorizations=authorizations)


def create_app():

 app = Flask(__name__)
 app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///QuickExam.db'
 app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 app.config['SWAGGER_UI_JSONEDITOR'] = True
 CORS(app)

 api.init_app(app)
 db.init_app(app)

 migrate = Migrate(app, db)

 return app

from .models import *
from .resources import *
