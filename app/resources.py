from flask_restplus import Resource, reqparse
from .app import api, db, app
from .models import *
import jwt
import datetime

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)

SECRET = 'RuloEsHermoso'

@api.route('/api/login')
class Token(Resource):
    def post(self):
        user_data = user_parser.parse_args()
        user = User.query.filter_by(username=user_data['username']).first()
        if user is None or not user.check_password(user_data['password']):
            return {'message': 'Invalid login'}, 401
        token = jwt.encode({
            'user':
            user.username,
            'exp':
            datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, SECRET)
        return {'token' : token.decode('UTF-8')}

@api.route('/api/register')
class UserRegister(Resource):
    def post(self):
        user_data = user_parser.parse_args()
        user = User(username=user_data['username'])
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({
            'user':
            user.username,
            'exp':
            datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, SECRET)
        return {'token' : token.decode('UTF-8')}
