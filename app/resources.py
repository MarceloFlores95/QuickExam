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
        return {'message': 'Successfully added Subject'}


@api.route('/api/topic')
class TopicViewAdd(Resource):
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
    @api.doc(security='apikey', params={'text': "The text of the question", 'topic_id': "The id of a topic"})
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


# QuestionMulti without the list of dummy answers
@api.route('/api/question/multi')
class QuestionMultiAdd(Resource):
    @api.doc(security='apikey',
             params={'text': "The text of the question", 'correct_answer': "The correct answer of the question",
                     'topic_id': "The id of a topic"})
    @token_check
    def post(self, user_id):
        question_multi_data = question_multi_parser.parse_args()
        question_multi = QuestionMulti(text=question_multi_data['text'],
                                       correct_answer=question_multi_data['correct_answer'],
                                       topic_id=question_multi_data['topic_id'])
        db.session.add(question_multi)
        db.session.commit()
        return {'message': 'Successfully added Multiple choice Question'}


# QuestionMulti WITH the list of dummy answers
# @api.route('/api/question/multi')
# class QuestionMultiAdd(Resource):
#     @api.doc(security='apikey',
#              params={'text': "The text of the question", 'correct_answer': "The correct answer of the question",
#                      'dummies': "Array with dummy answers for the question", 'topic_id': "The id of a topic"})
#     @token_check
#     def post(self, user_id):
#         question_multi_data = question_multi_parser.parse_args()
#         question_multi = QuestionMulti(text=question_multi_data['text'],
#                                        correct_answer=question_multi_data['correct_answer'], topic_id=['topic_id'])
#         db.session.add(question_multi)
#         for dummy in question_multi_data['dummies']:
#             dummy_answer = DummyAnswers(answer=dummy, question_id=question_multi.id)
#             db.session.add(dummy_answer)
#         db.session.commit()
#         return {'message': 'Successfully added Multiple choice Question'}


@api.route('/api/dummy_answers')
class DummyAnswersAdd(Resource):
    @api.doc(security='apikey', params={'question_multi_id': "The id of a multiple choice question"})
    @token_check
    def get(self, user_id):
        question_multi_id = flask.request.args.get('question_multi_id')
        question_multi = QuestionMulti.query.filter_by(id=question_multi_id).first()
        dummies = [dummy.get_parameters() for dummy in question_multi.dummy_questions]
        return dummies

    @api.doc(security='apikey', params={'answer': "The answer of the dummy answer",
                                        'question_id': "The id of the question the dummy answer belongs to"})
    @token_check
    def post(self, user_id):
        dummy_answer_data = dummy_answer_parser.parse_args()
        dummy_answer = DummyAnswers(answer=dummy_answer_data['answer'], question_id=dummy_answer_data['question_id'])
        db.session.add(dummy_answer)
        db.session.commit()
        return {'message': 'Successfully added Dummy Answer'}


@api.route('/api/variable')
class VariableViewAdd(Resource):
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
class TestViewAdd(Resource):
    @api.doc(security='apikey')
    @token_check
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        tests = [test.get_parameters() for test in user.tests]
        return tests

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
class TestQuestionsViewAdd(Resource):
    @api.doc(security='apikey', params={'test_id': "The id of a test"})
    @token_check
    def get(self, user_id):
        test_id = flask.request.args.get('test_id')
        test = Test.query.filter_by(id=test_id).first()
        test_questions = [test_question.get_parameters() for test_question in test.questions]
        return test_questions

    @api.doc(security='apikey',
             params={'topic_id': "The topic id of the test questions",
                     'count': "The amount of test questions for the topic",
                     'test_id': "The id of a test"})
    @token_check
    def post(self, user_id):
        test_questions_data = test_questions_parser.parse_args()
        test_questions = TestQuestions(topic_id=test_questions_data['topic_id'], count=test_questions_data['count'],
                                       test_id=test_questions_data['test_id'])
        db.session.add(test_questions)
        db.session.commit()
        return {'message': 'Successfully added Test Questions'}


# updates

@api.route('/api/update/user')
class UserUpdate(Resource):
    @api.doc(security='apikey', params={'username': "The username", 'password': "The password for the user"})
    @token_check
    def post(self, user_id):
        user_data = user_parser.parse_args()
        user = User.query.filter_by(id=user_id).first()
        user.username = user_data['username']
        user.set_password(user_data['password'])
        db.session.commit()
        token = create_token(user)
        return {'token': token.decode('UTF-8')}


@api.route('/api/update/subject')
class SubjectUpdate(Resource):
    @api.doc(security='apikey', params={'subject_id': "The id of the subject to update", 'name': "The subject's name"})
    @token_check
    def post(self, user_id):
        subject_data = subject_parser.parse_args()
        subject = Subject.query.filter_by(id=subject_data['subject_id']).first()
        subject.name = subject_data['name']
        db.session.commit()
        return {'message': 'Successfully updated Subject'}


@api.route('/api/update/topic')
class TopicUpdate(Resource):
    @api.doc(security='apikey', params={'topic_id': "The id of the topic to update", 'name': "The topic's name"})
    @token_check
    def post(self, user_id):
        topic_data = topic_parser.parse_args()
        topic = Topic.query.filter_by(id=topic_data['topic_id']).first()
        topic.name = topic_data['name']
        db.session.commit()
        return {'message': 'Successfully updated Topic'}


@api.route('/api/update/variable')
class VariableUpdate(Resource):
    @api.doc(security='apikey',
             params={'variable_id': "The id of the variable to update", 'values': "The values the variable can take",
                     'symbol': "The symbol to identify the variable", 'type': "The data type of the variable"})
    @token_check
    def post(self, user_id):
        variable_data = variable_parser.parse_args()
        variable = Variable.query.filter_by(id=variable_data['variable_id']).first()
        variable.values = variable_data['values']
        variable.symbol = variable_data['symbol']
        variable.type = variable_data['type']
        db.session.commit()
        return {'message': 'Successfully updated Variable'}


@api.route('/api/update/question/open')
class QuestionOpenUpdate(Resource):
    @api.doc(security='apikey',
             params={'question_open_id': "The id of the open question to update", 'text': 'The text of the question'})
    @token_check
    def post(self, user_id):
        question_open_data = question_open_parser.parse_args()
        question_open = QuestionOpen.query.filter_by(id=question_open_data['question_open_id']).first()
        question_open.text = question_open_data['text']
        db.session.commit()
        return {'message': 'Successfully updated Open Question'}


@api.route('/api/update/question/tf')
class QuestionTFUpdate(Resource):
    @api.doc(security='apikey',
             params={'question_tf_id': "The id of the true or false question to update",
                     'text': "The text of the question", 'expression': "The expression to evaluate for the answer"})
    @token_check
    def post(self, user_id):
        question_tf_data = question_tf_parser.parse_args()
        question_tf = QuestionTF.query.filter_by(id=question_tf_data['question_tf_id']).first()
        question_tf.text = question_tf_data['text']
        question_tf.expression = question_tf_data['expression']
        db.session.commit()
        return {'message': 'Successfully updated True or False Question'}


@api.route('/api/update/question/multi')
class QuestionMultiUpdate(Resource):
    @api.doc(security='apikey',
             params={'question_multi_id': "The id of the multiple choice question to update",
                     'text': "The text of the question", 'correct_answer': "The correct answer of the question"})
    @token_check
    def post(self, user_id):
        question_multi_data = question_multi_parser.parse_args()
        question_multi = QuestionMulti.query.filter_by(id=question_multi_data['question_multi_id']).first()
        question_multi.text = question_multi_data['text']
        question_multi.correct_answer = question_multi_data['correct_answer']
        db.session.commit()
        return {'message': 'Successfully updated Multiple Choice Question'}


@api.route('/api/update/dummy_answer')
class DummyAnswerUpdate(Resource):
    @api.doc(security='apikey',
             params={'dummy_answer_id': "The id of the dummy answer to update", 'answer': "The dummy answer"})
    @token_check
    def post(self, user_id):
        dummy_answer_data = dummy_answer_parser.parse_args()
        dummy_answer = DummyAnswers.query.filter_by(id=dummy_answer_data['dummy_answer_id']).first()
        dummy_answer.answer = dummy_answer_data['answer']
        db.session.commit()
        return {'message': 'Successfully updated Dummy Answer'}


@api.route('/api/update/test')
class TestUpdate(Resource):
    @api.doc(security='apikey',
             params={'test_id': "The id of test to update", 'name': "The name of the test",
                     'header': "The header for the test",
                     'count': "The amount of the test types to be generated for the test"})
    @token_check
    def post(self, user_id):
        test_data = test_parser.parse_args()
        test = Test.query.filter_by(id=test_data['test_id']).first()
        test.name = test_data['name']
        test.header = test_data['header']
        test.count = test_data['count']
        db.session.commit()
        return {'message': 'Successfully updated Test'}


@api.route('/api/update/test/questions')
class TestQuestionsUpdate(Resource):
    @api.doc(security='apikey', params={'test_questions_id': "The id of the test questions",
                                        'topic_id': "The topic id of the test questions",
                                        'count': "The amount of test questions for the topic"})
    @token_check
    def post(self, user_id):
        test_questions_data = test_questions_parser.parse_args()
        test_questions = TestQuestions.query.filter_by(id=test_questions_data['test_questions_id']).first()
        test_questions.topic_id = test_questions_data['topic_id']
        test_questions.count = test_questions_data['count']
        db.session.commit()
        return {'message': 'Successfully updated Test Questions'}


# deletes

@api.route('/api/delete/user')
class UserDelete(Resource):
    @api.doc(security='apikey', params={'username': 'The username of the user to delete'})
    @token_check
    def post(self, user_id):
        user_data = user_parser.parse_args()
        user = User.query.filter_by(username=user_data['username']).first()
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Successfully deleted User'}


@api.route('/api/delete/subject')
class SubjectDelete(Resource):
    @api.doc(security='apikey', params={'subject_id': "The id of a subject"})
    @token_check
    def post(self, user_id):
        subject_data = subject_parser.parse_args()
        subject = Subject.query.filter_by(id=subject_data['subject_id']).first()
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Successfully deleted Subject'}


@api.route('/api/delete/topic')
class TopicDelete(Resource):
    @api.doc(security='apikey', params={'topic_id': "The id of a topic"})
    @token_check
    def post(self, user_id):
        topic_data = topic_parser.parse_args()
        topic = Topic.query.filter_by(id=topic_data['topic_id']).first()
        db.session.delete(topic)
        db.session.commit()
        return {'message': 'Successfully deleted Topic'}


@api.route('/api/delete/variable')
class VariableDelete(Resource):
    @api.doc(security='apikey', params={'variable_id': "The id of a variable"})
    @token_check
    def post(self, user_id):
        variable_data = variable_parser.parse_args()
        variable = Variable.query.filter_by(id=variable_data['variable_id']).first()
        db.session.delete(variable)
        db.session.commit()
        return {'message': 'Successfully deleted Variable'}


@api.route('/api/delete/question/open')
class QuestionOpenDelete(Resource):
    @api.doc(security='apikey', params={'question_open_id': "The id of an open question"})
    @token_check
    def post(self, user_id):
        question_open_data = question_open_parser.parse_args()
        question_open = QuestionOpen.query.filter_by(id=question_open_data['question_open_id']).first()
        db.session.delete(question_open)
        db.session.commit()
        return {'message': 'Successfully deleted Open Question'}


@api.route('/api/delete/question/tf')
class QuestionTFDelete(Resource):
    @api.doc(security='apikey', params={'question_tf_id': "The id of a true or false question"})
    @token_check
    def post(self, user_id):
        question_tf_data = question_tf_parser.parse_args()
        question_tf = QuestionTF.query.filter_by(id=question_tf_data['question_tf_id']).first()
        db.session.delete(question_tf)
        db.session.commit()
        return {'message': 'Successfully deleted True or False Question'}


@api.route('/api/delete/question/multi')
class QuestionMultiDelete(Resource):
    @api.doc(security='apikey', params={'question_multi_id': "The id of a multiple choice question"})
    @token_check
    def post(self, user_id):
        question_multi_data = question_multi_parser.parse_args()
        question_multi = QuestionMulti.query.filter_by(id=question_multi_data['question_multi_id']).first()
        db.session.delete(question_multi)
        db.session.commit()
        return {'message': 'Successfully deleted Multiple Choice Question'}


@api.route('/api/delete/dummy_answer')
class DummyAnswerDelete(Resource):
    @api.doc(security='apikey', params={'dummy_answer_id': "The id of a dummy answer"})
    @token_check
    def post(self, user_id):
        dummy_answer_data = dummy_answer_parser.parse_args()
        dummy_answer = DummyAnswers.query.filter_by(id=dummy_answer_data['dummy_answer_id']).first()
        db.session.delete(dummy_answer)
        db.session.commit()
        return {'message': 'Successfully deleted Dummy Answer'}


@api.route('/api/delete/test')
class TestDelete(Resource):
    @api.doc(security='apikey', params={'test_id': "The id of a test"})
    @token_check
    def post(self, user_id):
        test_data = test_parser.parse_args()
        test = Test.query.filter_by(id=test_data['test_id']).first()
        db.session.delete(test)
        db.session.commit()
        return {'message': 'Successfully deleted Test'}


@api.route('/api/delete/test/questions')
class TestQuestionsDelete(Resource):
    @api.doc(security='apikey', params={'test_questions_id': "The id of the test questions"})
    @token_check
    def post(self, user_id):
        test_questions_data = test_questions_parser.parse_args()
        test_questions = TestQuestions.query.filter_by(id=test_questions_data['test_questions_id']).first()
        db.session.delete(test_questions)
        db.session.commit()
        return {'message': 'Successfully deleted Test Questions'}
