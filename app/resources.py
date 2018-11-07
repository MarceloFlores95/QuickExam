from flask_restplus import Resource
from .app import api, db, app
import flask
from .models import *
from .parsers import *
import jwt
import itertools
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
@api.doc(params={'username': 'The username', 'password': 'The password'})
class Token(Resource):
    def post(self):
        user_data = user_parser.parse_args()
        user = User.query.filter_by(username=user_data['username']).first()
        if user is None or not user.check_password(user_data['password']):
            return {'message': 'Invalid login'}, 401
        token = create_token(user)
        return {'token': token.decode('UTF-8')}


@api.route('/api/register')
@api.doc(params={'username': 'The username', 'password': 'The password'})
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

    @api.doc(security='apikey', params={'name': "The subject's name"})
    @token_check
    def post(self, user_id):
        subject_data = subject_parser.parse_args()
        subject = Subject(name=subject_data['name'], user_id=user_id)
        db.session.add(subject)
        db.session.commit()
        return {'message': 'Successfully added Subject'}


@api.route('/api/topic')
class TopicView(Resource):
    @api.doc(security='apikey', params={'subject_id': "The id of a subject"})
    @token_check
    def get(self, user_id):
        subject_id = flask.request.args.get('subject_id')
        subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
        topics = [topic.get_parameters() for topic in subject.topics]
        return topics

    @api.doc(security='apikey', params={'name': "The topic's name", 'subject_id': 'A subject id'})
    @token_check
    def post(self, user_id):
        topic_data = topic_parser.parse_args()
        topic = Topic(
            name=topic_data['name'], subject_id=topic_data['subject_id'])
        db.session.add(topic)
        db.session.commit()
        return {'message': 'Successfully added Topic'}


@api.route('/api/question')
class QuestionView(Resource):
    @api.doc(security='apikey', params={'topic_id': "The id of a topic"})
    @token_check
    def get(self, user_id):
        topic_id = flask.request.args.get('topic_id')
        topic = Topic.query.filter_by(id=topic_id).first()
        questions = [question.get_parameters() for question in
                     itertools.chain(topic.questions_multi, topic.questions_open, topic.questions_tf)]
        return questions


@api.route('/api/question/open')
class QuestionOpenAdd(Resource):
    @api.doc(security='apikey', params={'text': 'The text of the question', 'topic_id': "The id of a topic"})
    @token_check
    def post(self, user_id):
        question_open_data = question_open_parser.parse_args()
        question_open = QuestionOpen(text=question_open_data['text'], topic_id=question_open_data['topic_id'])
        db.session.add(question_open)
        db.session.commit()
        return {'message': 'Successfully added Open Question'}


@api.route('/api/question/tf')
class QuestionTFAdd(Resource):
    @api.doc(security='apikey',
             params={'text': "The text of the question", 'expression': "The expression to evaluate for the answer",
                     'topic_id': "The id of a topic"})
    @token_check
    def post(self, user_id):
        question_tf_data = question_tf_parser.parse_args()
        question_tf = QuestionTF(text=question_tf_data['text'], expression=question_tf_data['expression'],
                                 topic_id=question_tf_data['topic_id'])
        db.session.add(question_tf)
        db.session.commit()
        return {'message': 'Successfully added True or False Question'}


@api.route('/api/question/multi')
class QuestionMultiAdd(Resource):
    @api.doc(security='apikey',
             params={'text': "The text of the question", 'correct_answer': "The correct answer of the question",
                     'dummies': "Array with dummy answers for the question", 'topic_id': "The id of a topic"})
    @token_check
    def post(self, user_id):
        question_multi_data = question_multi_parser.parse_args()
        question_multi = QuestionMulti(text=question_multi_data['text'],
                                       correct_answer=question_multi_data['correct_answer'], topic_id=['topic_id'])
        db.session.add(question_multi)
        for dummy in question_multi_data['dummies']:
            dummy_answer = DummyAnswers(answer=dummy, question_id=question_multi.id)
            db.session.add(dummy_answer)
        db.session.commit()
        return {'message': 'Successfully added Multiple choice Question'}


@api.route('/api/variable')
class VariableView(Resource):
    @api.doc(security='apikey',
             params={'question_open_id': "The id of the open question the variable belongs to (can be null)",
                     'question_tf_id': "The id of the true or false question the variable belongs to (can be null)",
                     'question_multi_id': "The id of the multiple choice question the variable belongs to (can be null)"})
    @token_check
    def get(self, user_id):
        question_open_id = flask.request.args.get('question_open_id')
        question_tf_id = flask.request.args.get('question_tf_id')
        question_multi_id = flask.request.args.get('question_multi_id')
        if question_open_id is not None:
            question_open = QuestionOpen.query.filter_by(id=question_open_id).first()
            variables = [variable.get_parameters() for variable in question_open.variables]
        elif question_tf_id is not None:
            question_tf = QuestionTF.query.filter_by(id=question_tf_id).first()
            variables = [variable.get_parameters() for variable in question_tf.variables]
        else:
            question_multi = QuestionMulti.query.filter_by(id=question_multi_id).first()
            variables = [variable.get_parameters() for variable in question_multi.variables]
        return variables

    @api.doc(security='apikey',
             params={'values': "The values the variable can take", 'symbol': "The symbol to identify the variable",
                     'type': "The data type of the variable",
                     'question_open_id': "The id of the open question the variables belongs to (can be null)",
                     'question_tf_id': "The id of the true or false question the variables belongs to (can be null)",
                     'question_multi_id': "The id of the multiple choice question the variables belongs to (can be null)"})
    @token_check
    def post(self, user_id):
        variable_data = variable_parser.parse_args()
        variable = Variable(values=variable_data['values'], symbol=variable_data['symbol'], type=variable_data['type'],
                            question_open_id=variable_data.get('question_open_id'),
                            question_tf_id=variable_data.get('question_tf_id'),
                            question_multi_id=variable_data.get('question_multi_id'))
        db.session.add(variable)
        db.session.commit()
        return {'message': 'Successfully added Variable'}


@api.route('/api/test')
class TestView(Resource):
    @api.doc(security='apikey',
             params={'name': "The name of the test", 'header': "The header for the test",
                     'count': "The amount of the test types to be generated for the test"})
    @token_check
    def post(self, user_id):
        test_data = test_parser.parse_args()
        test = Test(name=test_data['name'], header=test_data['header'], count=test_data['count'], user_id=user_id)
        db.session.add(test)
        db.session.commit()
        return {'message': 'Successfully added Test'}


@api.route('/api/test/questions')
class TestQuestionsAdd(Resource):
    @api.doc(security='apikey',
             params={'topic_id': "The topic id of the test questions", 'count': "The amount of test questions for the topic",
                     'test_id': "The id of a test"})
    @token_check
    def post(self, user_id):
        test_questions_data = test_questions_parser.parse_args()
        test_questions = TestQuestions(topic_id=test_questions_data['topic_id'], count=test_questions_data['count'],
                                       test_id=test_questions_data['test_id'])
        db.session.add(test_questions)
        db.session.commit()
        return {'message': 'Successfully added Test Questions'}


@api.route('/api/delete/user')
class UserDelete(Resource):
    @api.doc(security='apikey', params={'username': 'The username'})
    @token_check
    def post(self, user_id):
        user_data = user_parser.parse_args()
        user = User(username=user_data['username'])
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Successfully deleted User'}


@api.route('/api/delete/subject')
class UserSubject(Resource):
    @api.doc(security='apikey', params={'subject_id': "The id of a subject"})
    @token_check
    def post(self, user_id):
        subject_data = topic_parser.parse_args()
        subject = Subject.query.filter_by(id=subject_data['subject_id'])
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Successfully deleted Subject'}
