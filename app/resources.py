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
        token = flask.request.headers.get('X-API-KEY')
        try:
            data = jwt.decode(token, SECRET)
        except:
            return {'message': 'Invalid token'}, 401
        return func(*args, user_id=data['user_id'], **kwargs)

    return wrapper


@api.route('/api/login')
@api.doc(params={'username' : 'The username', 'password' : 'The password'})
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
        token = create_token(user)
        return {'token': token.decode('UTF-8')}


@api.route('/api/subject')
class SubjectView(Resource):
    @api.doc(security='apikey')
    @token_check
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        subjects = [subject.get_parameters() for subject in user.subjects]
        return subjects

    @api.doc(security='apikey', params={'name' : "The subject's name"})
    @token_check
    def post(self, user_id):
        subject_data = subject_parser.parse_args()
        subject = Subject(name=subject_data['name'], user_id=user_id)
        db.session.add(subject)
        db.session.commit()
        return {'message': 'Successfully added Subject'}


@api.route('/api/topic')
class TopicView(Resource):

    @api.doc(security='apikey', params={'subject_id' : "The id of a subject"})
    @token_check
    def get(self, user_id):
        subject_id = flask.request.args.get('subject_id')
        subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
        topics = [topic.get_parameters() for topic in subject.topics]
        return topics

    @api.doc(security='apikey', params={'name' : "The topic's name", 'subject_id' : 'A subject id'})
    @token_check
    def post(self):
        topic_data = topic_parser.parse_args()
        topic = Topic(
                name=topic_data['name'], subject_id=topic_data['subject_id'])
        db.session.add(topic)
        db.session.commit()
        return {'message': 'Successfully added Topic'}
