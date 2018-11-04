from flask_restplus import Resource
from .app import api, db, app
import flask
from .models import *
from .parsers import *
import jwt
import datetime

SECRET = 'RuloEsHermoso'


def create_token(user):
    token = jwt.encode(
        {
            'username': user.username,
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, SECRET)
    return token


def token_check(func):
    def wrapper(*args, **kwargs):
        token = flask.request.args.headers('X-API-KEY')
        try:
            data = jwt.decode(token, SECRET)
        except:
            return {'message': 'Invalid token'}, 401
        return func(user_id=data['user_id'], *args, **kwargs)

    return wrapper


@api.route('/api/login')
class Token(Resource):
    def post(self):
        user_data = user_parser.parse_args()
        user = User.query.filter_by(username=user_data['username']).first()
        if user is None or not user.check_password(user_data['password']):
            return {'message': 'Invalid login'}, 401
        token = create_token(user)
        return {'token': token.decode('UTF-8')}


@api.route('/api/register')
class UserRegister(Resource):
    def post(self):
        user_data = user_parser.parse_args()
        user = User(username=user_data['username'])
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.commit()
        token = create_token(token)
        return {'token': token.decode('UTF-8')}


@api.route('/api/subject/<string:token>')
class SubjectView(Resource):
    def get(self, token):
        data = token_check(token)
        if data:
            user = User.query.filter_by(id=data['user_id']).first()
            subjects = [subject.get_parameters() for subject in user.subjects]
            return subjects
        else:
            return {'message': 'Invalid token'}, 401

    def post(self, token):
        data = token_check(token)
        if data:
            subject_data = subject_parser.parse_args()
            subject = Subject(
                name=subject_data['name'], user_id=data['user_id'])
            db.session.add(subject)
            db.session.commit()
            return {'message': 'Successfully added Subject'}
        else:
            return {'message': 'Invalid token'}, 401


@api.route('/api/topic/<string:token>')
class TopicView(Resource):
    def get(self, token):
        data = token_check(token)
        if data:
            subject_id = flask.request.args.get('subject_id')
            subject = Subject.query.filter_by(id=subject_id).first()
            topics = [topic.get_parameters() for topic in subject.topics]
            return topics
        else:
            return {'message': 'Invalid token'}, 401

    def post(self, token):
        data = token_check(token)
        if data:
            topic_data = topic_parser.parse_args()
            topic = Topic(
                name=topic_data['name'], subject_id=topic_data['subject_id'])
            db.session.add(topic)
            db.session.commit()
            return {'message': 'Successfully added Topic'}
        else:
            return {'message': 'Invalid token'}, 401
