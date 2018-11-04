from flask_restplus import Resource
from .app import api, db, app
import flask
from .models import *
from .parsers import user_parser
import jwt
import datetime

SECRET = 'RuloEsHermoso'


def token_check(token):
    try:
        data = jwt.decode(token, SECRET)
    except:
        return None
    return data


@api.route('/api/login')
class Token(Resource):
    def post(self):
        user_data = user_parser.parse_args()
        user = User.query.filter_by(username=user_data['username']).first()
        if user is None or not user.check_password(user_data['password']):
            return {'message': 'Invalid login'}, 401
        token = jwt.encode(
            {
                'user': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, SECRET)
        return {'token': token.decode('UTF-8')}


@api.route('/api/register')
class UserRegister(Resource):
    def post(self):
        user_data = user_parser.parse_args()
        user = User(username=user_data['username'])
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.commit()
        token = jwt.encode(
            {
                'user': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, SECRET)
        return {'token': token.decode('UTF-8')}


@api.route('/api/subject/<string:token>')
class SubjectView(Resource):
    def get(self, token):
        data = token_check(token)
        if data:
            user = User.query.filter_by(username=data['user']).first()
            subjects = [subject.get_parameters() for subject in user.subjects]
            return subjects
        else:
            return {'message': 'Invalid token'}, 401


@api.route('/api/topic/<string:token>')
class TopicView(Resource):
    def get(self, token):
        data = token_check(token)
        if data:
            subject_id = flask.request.args.get('subject')
            subject = Subject.query.filter_by(id=subject_id).first()
            topics = [topic.get_parameters() for topic in subject.topics]
            return topics
        else:
            return {'message': 'Invalid token'}, 401
