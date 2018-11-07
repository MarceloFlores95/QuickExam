from flask_restplus import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)

subject_parser  = reqparse.RequestParser()
subject_parser.add_argument('name', type=str)

topic_parser = reqparse.RequestParser()
topic_parser.add_argument('name', type=str)
topic_parser.add_argument('subject_id', type=int)

question_open_parser = reqparse.RequestParser()
question_open_parser.add_argument('text', type=str)
question_open_parser.add_argument('topic_id', type=int)

question_tf_parser = reqparse.RequestParser()
question_tf_parser.add_argument('text', type=str)
question_tf_parser.add_argument('expression', type=str)
question_tf_parser.add_argument('topic_id', type=int)

question_multi_parser = reqparse.RequestParser()
question_multi_parser.add_argument('text', type=str)
question_multi_parser.add_argument('correct_answer', type=str)
question_multi_parser.add_argument('dummies', type=list)
question_multi_parser.add_argument('topic_id', type=int)
