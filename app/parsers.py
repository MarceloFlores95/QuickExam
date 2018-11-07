from flask_restplus import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)

subject_parser  = reqparse.RequestParser()
subject_parser.add_argument('subject_id', type=int)
subject_parser.add_argument('name', type=str)

topic_parser = reqparse.RequestParser()
topic_parser.add_argument('topic_id', type=int)
topic_parser.add_argument('name', type=str)
topic_parser.add_argument('subject_id', type=int)

question_open_parser = reqparse.RequestParser()
question_open_parser.add_argument('question_open_id', type=int)
question_open_parser.add_argument('text', type=str)
question_open_parser.add_argument('topic_id', type=int)

question_tf_parser = reqparse.RequestParser()
question_tf_parser.add_argument('question_tf_id', type=int)
question_tf_parser.add_argument('text', type=str)
question_tf_parser.add_argument('expression', type=str)
question_tf_parser.add_argument('topic_id', type=int)

question_multi_parser = reqparse.RequestParser()
question_multi_parser.add_argument('question_multi_id', type=int)
question_multi_parser.add_argument('text', type=str)
question_multi_parser.add_argument('correct_answer', type=str)
question_multi_parser.add_argument('dummies', type=list, location='json')
question_multi_parser.add_argument('topic_id', type=int)

variable_parser = reqparse.RequestParser()
variable_parser.add_argument('variable_id', type=int)
variable_parser.add_argument('values', type=str)
variable_parser.add_argument('symbol', type=str)
variable_parser.add_argument('type', type=str)
variable_parser.add_argument('question_open_id', type=int)
variable_parser.add_argument('question_tf_id', type=int)
variable_parser.add_argument('question_multi_id', type=int)

test_parser = reqparse.RequestParser()
test_parser.add_argument('test_id', type=int)
test_parser.add_argument('name', type=str)
test_parser.add_argument('header', type=str)
test_parser.add_argument('count', type=int)

test_questions_parser = reqparse.RequestParser()
test_questions_parser.add_argument('test_questions_id', type=int)
test_questions_parser.add_argument('topic_id', type=int)
test_questions_parser.add_argument('count', type=int)
test_questions_parser.add_argument('test_id', type=int)

dummy_answer_parser = reqparse.RequestParser()
dummy_answer_parser.add_argument('dummy_answer_id', type=int)
dummy_answer_parser.add_argument('answer', type=str)
dummy_answer_parser.add_argument('question_id', type=int)
