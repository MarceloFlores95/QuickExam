from flask_restplus import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)

subject_parser  = reqparse.RequestParser()
subject_parser.add_argument('name', type=str)

topic_parser = reqparse.RequestParser()
topic_parser.add_argument('name', type=str)
topic_parser.add_argument('subject_id', type=str)
