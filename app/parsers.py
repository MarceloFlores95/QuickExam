from flask_restplus import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)
