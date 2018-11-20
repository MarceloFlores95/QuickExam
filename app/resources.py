from flask_restplus import Resource
from .app import api, db
import flask
from .models import *
from .parsers import *
import jwt
import itertools
import datetime
import os
import pylatex


def get_secret():
    Debug = os.environ.get('DEBUG', default='True')
    return 'RuloEsHermoso' if Debug.lower() in ('t',
                                                'true') else os.urandom(16)


SECRET_KEY = get_secret()


def create_token(user):
    token = jwt.encode(
        {
            'username': user.username,
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, SECRET_KEY)
    return token


def token_check(func):
    def wrapper(*args, **kwargs):
        token = flask.request.headers.get('X-API-KEY')
        try:
            data = jwt.decode(token, SECRET_KEY)
        except:
            return {'message': 'Invalid token'}, 401
        kwargs['user_id'] = data['user_id']
        return func(*args, **kwargs)

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


@api.route('/api/user')
class UserView(Resource):
    @api.doc(security='apikey')
    @token_check
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user.get_parameters()


@api.route('/api/subject')
class SubjectViewAdd(Resource):
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
        return subject.get_parameters()


@api.route('/api/topic')
class TopicViewAdd(Resource):
    @api.doc(security='apikey', params={'subject_id': "The id of a subject"})
    @token_check
    def get(self, user_id):
        subject_id = flask.request.args.get('subject_id')
        subject = Subject.query.filter_by(
            id=subject_id, user_id=user_id).first()
        if subject is not None:
            topics = [topic.get_parameters() for topic in subject.topics]
            return topics
        else:
            return {'message': 'Subject does not belong to the user'}, 401

    @api.doc(
        security='apikey',
        params={
            'name': "The topic's name",
            'subject_id': 'A subject id'
        })
    @token_check
    def post(self, user_id):
        topic_data = topic_parser.parse_args()
        subject = Subject.query.filter_by(
            id=topic_data['subject_id'], user_id=user_id).first()
        if subject is not None:
            topic = Topic(
                name=topic_data['name'], subject_id=topic_data['subject_id'])
            db.session.add(topic)
            db.session.commit()
            return topic.get_parameters()
        else:
            return {'message': 'Subject does not belong to the user'}, 401


@api.route('/api/question')
class QuestionView(Resource):
    @api.doc(security='apikey', params={'topic_id': "The id of a topic"})
    @token_check
    def get(self, user_id):
        topic_id = flask.request.args.get('topic_id')
        topic = Topic.query.filter_by(id=topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            questions = [
                question.get_parameters() for question in itertools.chain(
                    topic.questions_multi, topic.questions_open, topic.
                    questions_tf)
            ]
            return questions
        else:
            return {'message': 'Topic does not belong to the user'}, 401


@api.route('/api/question/open')
class QuestionOpenAdd(Resource):
    @api.doc(
        security='apikey',
        params={
            'text': 'The text of the question',
            'topic_id': "The id of a topic"
        })
    @token_check
    def post(self, user_id):
        question_open_data = question_open_parser.parse_args()
        variables = question_open_data.get('variables', [])
        topic = Topic.query.filter_by(
            id=question_open_data['topic_id']).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            question_open = QuestionOpen(
                text=question_open_data['text'],
                topic_id=question_open_data['topic_id'])
            db.session.add(question_open)
            db.session.commit()
            for variable in variables:
                new_variable = Variable(
                    values=variable[0],
                    symbol=variable[1],
                    type=variable[2],
                    question_open_id=question_open.id)
                db.session.add(new_variable)
            db.session.commit()
            return question_open.get_parameters()
        else:
            return {'message': 'Topic does not belong to the user'}, 401


@api.route('/api/question/tf')
class QuestionTFAdd(Resource):
    @api.doc(
        security='apikey',
        params={
            'text': "The text of the question",
            'expression': "The expression to evaluate for the answer",
            'topic_id': "The id of a topic"
        })
    @token_check
    def post(self, user_id):
        question_tf_data = question_tf_parser.parse_args()
        variables = question_tf_data.get('variables', [])
        topic = Topic.query.filter_by(id=question_tf_data['topic_id']).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            question_tf = QuestionTF(
                text=question_tf_data['text'],
                expression=question_tf_data['expression'],
                topic_id=question_tf_data['topic_id'])
            db.session.add(question_tf)
            db.session.commit()
            for variable in variables:
                new_variable = Variable(
                    values=variable[0],
                    symbol=variable[1],
                    type=variable[2],
                    question_tf_id=question_tf.id)
                db.session.add(new_variable)
            db.session.commit()
            return question_tf.get_parameters()
        else:
            return {'message': 'Topic does not belong to the user'}, 401


@api.route('/api/question/multi')
class QuestionMultiAdd(Resource):
    @api.doc(
        security='apikey',
        params={
            'text': "The text of the question",
            'correct_answer': "The correct answer of the question",
            'topic_id': "The id of a topic"
        })
    @token_check
    def post(self, user_id):
        question_multi_data = question_multi_parser.parse_args()
        variables = question_multi_data.get('variables', [])
        print(variables)
        topic = Topic.query.filter_by(
            id=question_multi_data['topic_id']).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        dummies = question_multi_data.get('dummies', [])
        if subject is not None:
            question_multi = QuestionMulti(
                text=question_multi_data['text'],
                correct_answer=question_multi_data['correct_answer'],
                topic_id=question_multi_data['topic_id'])
            db.session.add(question_multi)
            db.session.commit()
            for variable in variables:
                new_variable = Variable(
                    values=variable[0],
                    symbol=variable[1],
                    type=variable[2],
                    question_multi_id=question_multi.id)
                print(new_variable)
                db.session.add(new_variable)
            for dummy_text in dummies:
                dummy = DummyAnswers(
                    answer=dummy_text, question_id=question_multi.id)
                db.session.add(dummy)
            db.session.commit()
            return question_multi.get_parameters()
        else:
            return {'message': 'Topic does not belong to the user'}, 401


@api.route('/api/dummy_answers')
class DummyAnswersAdd(Resource):
    @api.doc(
        security='apikey',
        params={'question_multi_id': "The id of a multiple choice question"})
    @token_check
    def get(self, user_id):
        question_multi_id = flask.request.args.get('question_multi_id')
        question_multi = QuestionMulti.query.filter_by(
            id=question_multi_id).first()
        topic = Topic.query.filter_by(id=question_multi.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            dummies = [
                dummy.get_parameters()
                for dummy in question_multi.dummy_questions
            ]
            return dummies
        else:
            return {'message': 'Question does not belong to the user'}, 401

    @api.doc(
        security='apikey',
        params={
            'answer': "The answer of the dummy answer",
            'question_id': "The id of the question the dummy answer belongs to"
        })
    @token_check
    def post(self, user_id):
        dummy_answer_data = dummy_answer_parser.parse_args()
        question_multi = QuestionMulti.query.filter_by(
            id=dummy_answer_data['question_id']).first()
        topic = Topic.query.filter_by(id=question_multi.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            dummy_answer = DummyAnswers(
                answer=dummy_answer_data['answer'],
                question_id=dummy_answer_data['question_id'])
            db.session.add(dummy_answer)
            db.session.commit()
            return dummy_answer.get_parameters()
        else:
            return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/variable')
class VariableViewAdd(Resource):
    @api.doc(
        security='apikey',
        params={
            'question_open_id':
            "The id of the open question the variable belongs to (can be null)",
            'question_tf_id':
            "The id of the true or false question the variable belongs to (can be null)",
            'question_multi_id':
            "The id of the multiple choice question the variable belongs to (can be null)"
        })
    @token_check
    def get(self, user_id):
        question_open_id = flask.request.args.get('question_open_id')
        question_tf_id = flask.request.args.get('question_tf_id')
        question_multi_id = flask.request.args.get('question_multi_id')
        if question_open_id is not None:
            question_open = QuestionOpen.query.filter_by(
                id=question_open_id).first()
            topic = Topic.query.filter_by(id=question_open.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is not None:
                variables = [
                    variable.get_parameters()
                    for variable in question_open.variables
                ]
            else:
                return {'message': 'Question does not belong to the user'}, 401
        elif question_tf_id is not None:
            question_tf = QuestionTF.query.filter_by(id=question_tf_id).first()
            topic = Topic.query.filter_by(id=question_tf.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is not None:
                variables = [
                    variable.get_parameters()
                    for variable in question_tf.variables
                ]
            else:
                return {'message': 'Question does not belong to the user'}, 401
        else:
            question_multi = QuestionMulti.query.filter_by(
                id=question_multi_id).first()
            topic = Topic.query.filter_by(id=question_multi.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is not None:
                variables = [
                    variable.get_parameters()
                    for variable in question_multi.variables
                ]
            else:
                return {'message': 'Question does not belong to the user'}, 401
        return variables

    @api.doc(
        security='apikey',
        params={
            'values':
            "The values the variable can take",
            'symbol':
            "The symbol to identify the variable",
            'type':
            "The data type of the variable",
            'question_open_id':
            "The id of the open question the variables belongs to (can be null)",
            'question_tf_id':
            "The id of the true or false question the variables belongs to (can be null)",
            'question_multi_id':
            "The id of the multiple choice question the variables belongs to (can be null)"
        })
    @token_check
    def post(self, user_id):
        variable_data = variable_parser.parse_args()
        if variable_data.get('question_open_id') is not None:
            question_open = QuestionOpen.query.filter_by(
                id=variable_data.get('question_open_id')).first()
            topic = Topic.query.filter_by(id=question_open.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is not None:
                variable = Variable(
                    values=variable_data['values'],
                    symbol=variable_data['symbol'],
                    type=variable_data['type'],
                    question_open_id=variable_data.get('question_open_id'),
                    question_tf_id=variable_data.get('question_tf_id'),
                    question_multi_id=variable_data.get('question_multi_id'))
                db.session.add(variable)
                db.session.commit()
                return variable.get_parameters()
            else:
                return {'message': 'Question does not belong to the user'}, 401
        elif variable_data.get('question_tf_id') is not None:
            question_tf = QuestionTF.query.filter_by(
                id=variable_data.get('question_tf_id')).first()
            topic = Topic.query.filter_by(id=question_tf.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is not None:
                variable = Variable(
                    values=variable_data['values'],
                    symbol=variable_data['symbol'],
                    type=variable_data['type'],
                    question_open_id=variable_data.get('question_open_id'),
                    question_tf_id=variable_data.get('question_tf_id'),
                    question_multi_id=variable_data.get('question_multi_id'))
                db.session.add(variable)
                db.session.commit()
                return variable.get_parameters()
            else:
                return {'message': 'Question does not belong to the user'}, 401
        else:
            question_multi = QuestionMulti.query.filter_by(
                id=variable_data.get('question_multi_id')).first()
            topic = Topic.query.filter_by(id=question_multi.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is not None:
                variable = Variable(
                    values=variable_data['values'],
                    symbol=variable_data['symbol'],
                    type=variable_data['type'],
                    question_open_id=variable_data.get('question_open_id'),
                    question_tf_id=variable_data.get('question_tf_id'),
                    question_multi_id=variable_data.get('question_multi_id'))
                db.session.add(variable)
                db.session.commit()
                return variable.get_parameters()
            else:
                return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/test')
class TestViewAdd(Resource):
    @api.doc(security='apikey')
    @token_check
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        tests = [test.get_parameters() for test in user.tests]
        return tests

    @api.doc(
        security='apikey',
        params={
            'name': "The name of the test",
            'header': "The header for the test",
            'count':
            "The amount of the test types to be generated for the test"
        })
    @token_check
    def post(self, user_id):
        test_data = test_parser.parse_args()
        test = Test(
            name=test_data['name'],
            header=test_data['header'],
            count=test_data['count'],
            user_id=user_id)
        db.session.add(test)
        db.session.commit()
        for question in test_data.get('questions', []):
            test_question = TestQuestions(
                topic_id=question[0], count=question[1], test_id=test.id)
            db.session.add(test_question)
        db.session.commit()
        return test.get_parameters()


@api.route('/api/test/questions')
class TestQuestionsViewAdd(Resource):
    @api.doc(security='apikey', params={'test_id': "The id of a test"})
    @token_check
    def get(self, user_id):
        test_id = flask.request.args.get('test_id')
        test = Test.query.filter_by(id=test_id, user_id=user_id).first()
        if test is not None:
            test_questions = [
                test_question.get_parameters()
                for test_question in test.questions
            ]
            return test_questions
        else:
            return {'message': 'Test does not belong to the user'}, 401

    @api.doc(
        security='apikey',
        params={
            'topic_id': "The topic id of the test questions",
            'count': "The amount of test questions for the topic",
            'test_id': "The id of a test"
        })
    @token_check
    def post(self, user_id):
        test_questions_data = test_questions_parser.parse_args()
        test = Test.query.filter_by(
            id=test_questions_data['test_id'], user_id=user_id).first()
        if test is None:
            return {'message': 'Test does not belong to the user'}, 401
        topic = Topic.query.filter_by(
            id=test_questions_data['topic_id']).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is None:
            return {'message': 'Topic does not belong to the user'}, 401
        test_questions = TestQuestions(
            topic_id=test_questions_data['topic_id'],
            count=test_questions_data['count'],
            test_id=test_questions_data['test_id'])
        db.session.add(test_questions)
        db.session.commit()
        return test_questions.get_parameters()


@api.route('/api/generate_tests')
class TestGenerator(Resource):
    @api.doc(security='apikey', params={'test_id': 'ID of a test'})
    def get(self):
        test = Test.query.filter_by(
            id=flask.request.args.get('test_id')).first()
        if test is not None:
            doc = test.create_pdf()
            pdf_name = f'{test.name}-{datetime.datetime.now()}'
            doc.generate_pdf(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__), '..', 'pdfs', pdf_name)))
            return flask.send_file(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__), '..', 'pdfs',
                        pdf_name + '.pdf')),
                as_attachment=True)
    '''@token_check
    def post(self, user_id):
        if 'test_id' not in flask.request.args:
            return {'message': 'Invalid test ID'}, 500
        user = User.query.filter_by(id=user_id).first()
        test = Test.query.filter_by(
            id=flask.request.args.get('test_id'), user_id=user_id).first()
        if test is not None:
            doc = test.create_pdf()
            pdf_name = f'{test.name}-{user.username}-{datetime.datetime.now()}'
            doc.generate_pdf(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__), '..', 'pdfs', pdf_name)))
            return flask.send_file(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__), '..', 'pdfs',
                        pdf_name + '.pdf')),
                as_attachment=True)
        else:
            return {'message': 'Test does not belong to the user'}, 401'''


# updates


@api.route('/api/update/user')
class UserUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'username': "The username",
            'password': "The password for the user"
        })
    @token_check
    def post(self, user_id):
        user_data = user_parser.parse_args()
        user = User.query.filter_by(id=user_id).first()
        user.username = user_data['username']
        user.set_password(user_data['password'])
        db.session.commit()
        token = create_token(user)
        user_parameters = user.get_parameters()
        user_parameters['token'] = token.decode('UTF-8')
        return user_parameters


@api.route('/api/update/subject')
class SubjectUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'subject_id': "The id of the subject to update",
            'name': "The subject's name"
        })
    @token_check
    def post(self, user_id):
        subject_data = subject_parser.parse_args()
        subject = Subject.query.filter_by(
            id=subject_data['subject_id'], user_id=user_id).first()
        if subject is not None:
            subject.name = subject_data['name']
            db.session.commit()
            return subject.get_parameters()
        else:
            return {'message': 'Subject does not belong to the user'}, 401


@api.route('/api/update/topic')
class TopicUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'topic_id': "The id of the topic to update",
            'name': "The topic's name"
        })
    @token_check
    def post(self, user_id):
        topic_data = topic_parser.parse_args()
        topic = Topic.query.filter_by(id=topic_data['topic_id']).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            topic.name = topic_data['name']
            db.session.commit()
            return topic.get_parameters()
        else:
            return {'message': 'Topic does not belong to the user'}, 401


@api.route('/api/update/variable')
class VariableUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'variable_id': "The id of the variable to update",
            'values': "The values the variable can take",
            'symbol': "The symbol to identify the variable",
            'type': "The data type of the variable"
        })
    @token_check
    def post(self, user_id):
        variable_data = variable_parser.parse_args()
        variable = Variable.query.filter_by(
            id=variable_data['variable_id']).first()
        if variable.question_open_id is not None:
            question_open = QuestionOpen.query.filter_by(
                id=variable.question_open_id).first()
            topic = Topic.query.filter_by(id=question_open.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is None:
                return {'message': 'Variable does not belong to the user'}, 401
        elif variable.question_tf_id is not None:
            question_tf = QuestionTF.query.filter_by(
                id=variable.question_tf_id).first()
            topic = Topic.query.filter_by(id=question_tf.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is None:
                return {'message': 'Variable does not belong to the user'}, 401
        elif variable.question_multi_id is not None:
            question_multi = QuestionMulti.query.filter_by(
                id=variable.question_multi_id).first()
            topic = Topic.query.filter_by(id=question_multi.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is None:
                return {'message': 'Variable does not belong to the user'}, 401
        variable.values = variable_data['values']
        variable.symbol = variable_data['symbol']
        variable.type = variable_data['type']
        db.session.commit()
        return variable.get_parameters()


@api.route('/api/update/question/open')
class QuestionOpenUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'question_open_id': "The id of the open question to update",
            'text': 'The text of the question'
        })
    @token_check
    def post(self, user_id):
        question_open_data = question_open_parser.parse_args()
        question_open = QuestionOpen.query.filter_by(
            id=question_open_data['question_open_id']).first()
        topic = Topic.query.filter_by(id=question_open.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            for variable in question_open.variables:
                db.session.delete(variable)
            for variable in question_open_data.get('variables', []):
                new_variable = Variable(
                    values=variable['values'],
                    symbol=variable['symbol'],
                    type=variable['type'],
                    question_open_id=question_open.id)
                db.session.add(new_variable)
            question_open.text = question_open_data['text']
            db.session.commit()
            return question_open.get_parameters()
        else:
            return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/update/question/tf')
class QuestionTFUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'question_tf_id': "The id of the true or false question to update",
            'text': "The text of the question",
            'expression': "The expression to evaluate for the answer"
        })
    @token_check
    def post(self, user_id):
        question_tf_data = question_tf_parser.parse_args()
        question_tf = QuestionTF.query.filter_by(
            id=question_tf_data['question_tf_id']).first()
        topic = Topic.query.filter_by(id=question_tf.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            for variable in question_tf.variables:
                db.session.delete(variable)
            for variable in question_tf_data.get('variables', []):
                new_variable = Variable(
                    values=variable['values'],
                    symbol=variable['symbol'],
                    type=variable['type'],
                    question_tf_id=question_tf.id)
                db.session.add(new_variable)
            question_tf.text = question_tf_data['text']
            question_tf.expression = question_tf_data['expression']
            db.session.commit()
            return question_tf.get_parameters()
        else:
            return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/update/question/multi')
class QuestionMultiUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'question_multi_id':
            "The id of the multiple choice question to update",
            'text':
            "The text of the question",
            'correct_answer':
            "The correct answer of the question"
        })
    @token_check
    def post(self, user_id):
        question_multi_data = question_multi_parser.parse_args()
        dummies_text = question_multi_data.get('dummies', [])
        question_multi = QuestionMulti.query.filter_by(
            id=question_multi_data['question_multi_id']).first()
        topic = Topic.query.filter_by(id=question_multi.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            for variable in question_multi.variables:
                db.session.delete(variable)
            for variable in question_multi_data.get('variables', []):
                new_variable = Variable(
                    values=variable['values'],
                    symbol=variable['symbol'],
                    type=variable['type'],
                    question_multi_id=question_multi.id)
                db.session.add(new_variable)
            for dummy in question_multi.dummy_questions:
                db.session.delete(dummy)
            question_multi.text = question_multi_data['text']
            question_multi.correct_answer = question_multi_data[
                'correct_answer']
            for dummy_text in dummies_text:
                db.session.add(
                    DummyAnswers(answer=dummy_text, question_id=question_multi.id))
            db.session.commit()
            return question_multi.get_parameters()
        else:
            return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/update/dummy_answer')
class DummyAnswerUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'dummy_answer_id': "The id of the dummy answer to update",
            'answer': "The dummy answer"
        })
    @token_check
    def post(self, user_id):
        dummy_answer_data = dummy_answer_parser.parse_args()
        dummy_answer = DummyAnswers.query.filter_by(
            id=dummy_answer_data['dummy_answer_id']).first()
        question_multi = QuestionMulti.query.filter_by(
            id=dummy_answer.question_id).first()
        topic = Topic.query.filter_by(id=question_multi.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            dummy_answer.answer = dummy_answer_data['answer']
            db.session.commit()
            return dummy_answer.get_parameters()
        else:
            return {'message': 'Dummy Answer does not belong to the user'}, 401


@api.route('/api/update/test')
class TestUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'test_id': "The id of test to update",
            'name': "The name of the test",
            'header': "The header for the test",
            'count':
            "The amount of the test types to be generated for the test"
        })
    @token_check
    def post(self, user_id):
        test_data = test_parser.parse_args()
        test = Test.query.filter_by(
            id=test_data['test_id'], user_id=user_id).first()
        if test is not None:
            test.name = test_data['name']
            test.header = test_data['header']
            test.count = test_data['count']
            db.session.commit()
            return test.get_parameters()
        else:
            return {'message': 'Test does not belong to the user'}, 401


@api.route('/api/update/test/questions')
class TestQuestionsUpdate(Resource):
    @api.doc(
        security='apikey',
        params={
            'test_questions_id': "The id of the test questions",
            'topic_id': "The topic id of the test questions",
            'count': "The amount of test questions for the topic"
        })
    @token_check
    def post(self, user_id):
        test_questions_data = test_questions_parser.parse_args()
        test_questions = TestQuestions.query.filter_by(
            id=test_questions_data['test_questions_id']).first()
        test = Test.query.filter_by(
            id=test_questions.test_id, user_id=user_id).first()
        if test is None:
            return {'message': 'Test Questions do not belong to the user'}, 401
        topic = Topic.query.filter_by(
            id=test_questions_data['topic_id']).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is None:
            return {'message': 'Topic does not belong to the user'}, 401
        else:
            test_questions.topic_id = test_questions_data['topic_id']
            test_questions.count = test_questions_data['count']
            db.session.commit()
            return test_questions.get_parameters()


# deletes


@api.route('/api/delete/user')
class UserDelete(Resource):
    @api.doc(security='apikey')
    @token_check
    def post(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return user.get_parameters()


@api.route('/api/delete/subject')
class SubjectDelete(Resource):
    @api.doc(security='apikey', params={'subject_id': "The id of a subject"})
    @token_check
    def post(self, user_id):
        subject_data = subject_parser.parse_args()
        subject = Subject.query.filter_by(
            id=subject_data['subject_id'], user_id=user_id).first()
        if subject is not None:
            db.session.delete(subject)
            db.session.commit()
            return subject.get_parameters()
        else:
            return {'message': 'Subject does not belong to the user'}, 401


@api.route('/api/delete/topic')
class TopicDelete(Resource):
    @api.doc(security='apikey', params={'topic_id': "The id of a topic"})
    @token_check
    def post(self, user_id):
        topic_data = topic_parser.parse_args()
        topic = Topic.query.filter_by(id=topic_data['topic_id']).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            db.session.delete(topic)
            db.session.commit()
            return topic.get_parameters()
        else:
            return {'message': 'Topic does not belong to the user'}, 401


@api.route('/api/delete/variable')
class VariableDelete(Resource):
    @api.doc(security='apikey', params={'variable_id': "The id of a variable"})
    @token_check
    def post(self, user_id):
        variable_data = variable_parser.parse_args()
        variable = Variable.query.filter_by(
            id=variable_data['variable_id']).first()
        if variable.question_open_id is not None:
            question_open = QuestionOpen.query.filter_by(
                id=variable.question_open_id).first()
            topic = Topic.query.filter_by(id=question_open.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is None:
                return {'message': 'Variable does not belong to the user'}, 401
        elif variable.question_tf_id is not None:
            question_tf = QuestionTF.query.filter_by(
                id=variable.question_tf_id).first()
            topic = Topic.query.filter_by(id=question_tf.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is None:
                return {'message': 'Variable does not belong to the user'}, 401
        elif variable.question_multi_id is not None:
            question_multi = QuestionMulti.query.filter_by(
                id=variable.question_multi_id).first()
            topic = Topic.query.filter_by(id=question_multi.topic_id).first()
            subject = Subject.query.filter_by(
                id=topic.subject_id, user_id=user_id).first()
            if subject is None:
                return {'message': 'Variable does not belong to the user'}, 401
        db.session.delete(variable)
        db.session.commit()
        return variable.get_parameters()


@api.route('/api/delete/question/open')
class QuestionOpenDelete(Resource):
    @api.doc(
        security='apikey',
        params={'question_open_id': "The id of an open question"})
    @token_check
    def post(self, user_id):
        question_open_data = question_open_parser.parse_args()
        question_open = QuestionOpen.query.filter_by(
            id=question_open_data['question_open_id']).first()
        topic = Topic.query.filter_by(id=question_open.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            db.session.delete(question_open)
            db.session.commit()
            return question_open.get_parameters()
        else:
            return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/delete/question/tf')
class QuestionTFDelete(Resource):
    @api.doc(
        security='apikey',
        params={'question_tf_id': "The id of a true or false question"})
    @token_check
    def post(self, user_id):
        question_tf_data = question_tf_parser.parse_args()
        question_tf = QuestionTF.query.filter_by(
            id=question_tf_data['question_tf_id']).first()
        topic = Topic.query.filter_by(id=question_tf.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            db.session.delete(question_tf)
            db.session.commit()
            return question_tf.get_parameters()
        else:
            return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/delete/question/multi')
class QuestionMultiDelete(Resource):
    @api.doc(
        security='apikey',
        params={'question_multi_id': "The id of a multiple choice question"})
    @token_check
    def post(self, user_id):
        question_multi_data = question_multi_parser.parse_args()
        question_multi = QuestionMulti.query.filter_by(
            id=question_multi_data['question_multi_id']).first()
        topic = Topic.query.filter_by(id=question_multi.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            db.session.delete(question_multi)
            db.session.commit()
            return question_multi.get_parameters()
        else:
            return {'message': 'Question does not belong to the user'}, 401


@api.route('/api/delete/dummy_answer')
class DummyAnswerDelete(Resource):
    @api.doc(
        security='apikey',
        params={'dummy_answer_id': "The id of a dummy answer"})
    @token_check
    def post(self, user_id):
        dummy_answer_data = dummy_answer_parser.parse_args()
        dummy_answer = DummyAnswers.query.filter_by(
            id=dummy_answer_data['dummy_answer_id']).first()
        question_multi = QuestionMulti.query.filter_by(
            id=dummy_answer.question_id).first()
        topic = Topic.query.filter_by(id=question_multi.topic_id).first()
        subject = Subject.query.filter_by(
            id=topic.subject_id, user_id=user_id).first()
        if subject is not None:
            db.session.delete(dummy_answer)
            db.session.commit()
            return dummy_answer.get_parameters()
        else:
            return {'message': 'Dummy Answer does not belong to the user'}, 401


@api.route('/api/delete/test')
class TestDelete(Resource):
    @api.doc(security='apikey', params={'test_id': "The id of a test"})
    @token_check
    def post(self, user_id):
        test_data = test_parser.parse_args()
        test = Test.query.filter_by(
            id=test_data['test_id'], user_id=user_id).first()
        if test is not None:
            db.session.delete(test)
            db.session.commit()
            return test.get_parameters()
        else:
            return {'message': 'Test does not belong to the user'}, 401


@api.route('/api/delete/test/questions')
class TestQuestionsDelete(Resource):
    @api.doc(
        security='apikey',
        params={'test_questions_id': "The id of the test questions"})
    @token_check
    def post(self, user_id):
        test_questions_data = test_questions_parser.parse_args()
        test_questions = TestQuestions.query.filter_by(
            id=test_questions_data['test_questions_id']).first()
        test = Test.query.filter_by(
            id=test_questions.test_id, user_id=user_id).first()
        if test is not None:
            db.session.delete(test_questions)
            db.session.commit()
            return test_questions.get_parameters()
        else:
            return {'message': 'Test Questions do not belong to the user'}, 401
