from .app import db
from typing import Any, Dict, Union
from decimal import Decimal, getcontext, ROUND_HALF_UP
from werkzeug.security import generate_password_hash, check_password_hash
from pylatex import Subsection
import random
import re
from evaluator import QuestionParser, BooleanParser
from pylatex import Document, Enumerate, Section, NewPage, LineBreak, Command, Package, NoEscape, HugeText, Center, FlushRight, LargeText
from pylatex.utils import bold
import functools

getcontext().rounding = ROUND_HALF_UP
getcontext().prec = 8


class Subject(db.Model):
    __tablename__ = 'Subject'
    __table_args__ = (db.UniqueConstraint('name', 'user_id'), )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topics = db.relationship('Topic', cascade='all')
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "subject_id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "topics": [topic.get_parameters() for topic in self.topics]
        }


class Topic(db.Model):
    __tablename__ = 'Topic'
    __table_args__ = (db.UniqueConstraint('name', 'subject_id'), )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(
        db.Integer, db.ForeignKey('Subject.id'), nullable=False)
    questions_open = db.relationship('QuestionOpen', cascade='all')
    questions_tf = db.relationship('QuestionTF', cascade='all')
    questions_multi = db.relationship('QuestionMulti', cascade='all')
    test_questions = db.relationship('TestQuestions', cascade='all')

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "topic_id":
            self.id,
            "name":
            self.name,
            "subject_id":
            self.subject_id,
            "questions_open": [
                question_open.get_parameters()
                for question_open in self.questions_open
            ],
            "questions_tf": [
                question_tf.get_parameters()
                for question_tf in self.questions_tf
            ],
            "questions_multi": [
                question_multi.get_parameters()
                for question_multi in self.questions_multi
            ]
        }


class Variable(db.Model):
    __tablename__ = 'Variable'
    id = db.Column(db.Integer, primary_key=True)
    values = db.Column(db.String(2000), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    question_open_id = db.Column(db.Integer, db.ForeignKey('QuestionOpen.id'))
    question_tf_id = db.Column(db.Integer, db.ForeignKey('QuestionTF.id'))
    question_multi_id = db.Column(db.Integer,
                                  db.ForeignKey('QuestionMulti.id'))

    def get_parameters(self):
        return {
            "variable_id": self.id,
            "values": self.values,
            "symbol": self.symbol,
            "type": self.type,
            "question_open_id": self.question_open_id,
            "question_tf_id": self.question_tf_id,
            "question_multi_id": self.question_multi_id
        }

    @property
    def value(self) -> Union[int, str, Decimal]:
        values = self.values.split(',')
        value = random.choice(values)
        if re.match(r'\d+-\d+', value):
            splited_values = value.split('-')
            return random.randint(
                int(splited_values[0]), int(splited_values[1]))
        if self.type == 'int':
            return int(value)
        if self.type == 'dec':
            return Decimal(value)
        return value


class QuestionOpen(db.Model):
    __tablename__ = 'QuestionOpen'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "question_open_id": self.id,
            "text": self.text,
            "topic_id": self.topic_id,
            "variables":
            [variable.get_parameters() for variable in self.variables]
        }

    def append_to_document(self, doc: Document,
                           doc_answers: Enumerate) -> None:
        variable_dict = {}
        for variable in self.variables:
            variable_dict[variable.symbol] = variable.value
        parsed_text = QuestionParser(**variable_dict).parse(self.text)
        with doc.create(Section(parsed_text)):
            doc.append('Respuesta: ')
            doc.append(LineBreak())
        doc_answers.add_item('Respuesta de pregunta abierta')


class QuestionTF(db.Model):
    __tablename__ = 'QuestionTF'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    expression = db.Column(db.String(1000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "question_tf_id": self.id,
            "text": self.text,
            "expression": self.expression,
            "topic_id": self.topic_id,
            "variables":
            [variable.get_parameters() for variable in self.variables]
        }

    def append_to_document(self, doc: Document,
                           doc_answers: Enumerate) -> None:
        variable_dict = {}
        for variable in self.variables:
            variable_dict[variable.symbol] = variable.value
        parsed_text = QuestionParser(**variable_dict).parse(self.text)
        with doc.create(Section(parsed_text)):
            doc.append(bold('Verdadero\t\tFalso'))
        expr = BooleanParser(**variable_dict).parse(self.expression)
        doc_answers.add_item('VERDADERO' if expr else 'FALSO')


class QuestionMulti(db.Model):
    __tablename__ = 'QuestionMulti'
    id = db.Column(db.Integer, primary_key=True)
    correct_answer = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')
    dummy_questions = db.relationship('DummyAnswers', cascade='all')

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "question_multi_id":
            self.id,
            "correct_answer":
            self.correct_answer,
            "text":
            self.text,
            "topic_id":
            self.topic_id,
            "variables":
            [variable.get_parameters() for variable in self.variables],
            "dummies":
            [dummy.get_parameters() for dummy in self.dummy_questions]
        }

    def append_to_document(self, doc: Document, doc_answers: Enumerate):
        variable_dict = {}
        for variable in self.variables:
            variable_dict[variable.symbol] = variable.value
        question_parser = QuestionParser(**variable_dict)
        parsed_text = question_parser.parse(self.text)
        correct_answer = question_parser.parse(self.correct_answer)
        answers = list(
            map(question_parser.parse,
                map(lambda x: x.answer, self.dummy_questions)))
        random.shuffle(answers)
        correct_pos = random.randint(0, len(answers))
        answers.insert(correct_pos, correct_answer)
        with doc.create(Section(parsed_text)):
            with doc.create(
                    Enumerate(
                        enumeration_symbol=r'\alph*) ', options={'start':
                                                                 1})) as enum:
                for answer in answers:
                    enum.add_item(answer)
        doc_answers.add_item(chr(ord('a') + correct_pos))


class DummyAnswers(db.Model):
    __tablename__ = 'DummyAnswers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000), nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey('QuestionMulti.id'), nullable=False)

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "dummy_answer_id": self.id,
            "answer": self.answer,
            "question_id": self.question_id
        }


class Test(db.Model):
    __tablename__ = 'Test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    header = db.Column(db.String(10000), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    questions = db.relationship('TestQuestions', cascade='all')
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "test_id":
            self.id,
            "name":
            self.name,
            "header":
            self.header,
            "count":
            self.count,
            "user_id":
            self.user_id,
            "test_questions":
            [question.get_parameters() for question in self.questions]
        }

    def create_pdf(self) -> Document:
        questions = functools.reduce(
            lambda a, b: a + b, map(lambda x: x.get_questions(),
                                    self.questions), [])
        doc = Document()
        doc.preamble.append(Package('titling'))
        for i in range(1, self.count + 1):
            random.shuffle(questions)
            with doc.create(Center()):
                doc.append(HugeText(self.header))
            doc.append(bold('Nombre:'))
            doc.append(LineBreak())
            doc.append(bold('ID:'))
            doc.append(LineBreak())
            with doc.create(FlushRight()):
                doc.append(LargeText(f'Examen tipo {i}'))
            enum = Enumerate()
            for question in questions:
                question.append_to_document(doc, enum)
            doc.append(NewPage())
            doc.append('Guía de respuestas')
            doc.append(enum)
            doc.append(NewPage())
            doc.append(Command('setcounter', ['section', '0']))
        return doc


class TestQuestions(db.Model):
    __tablename__ = 'TestQuestions'
    __table_args__ = (db.UniqueConstraint('topic_id', 'test_id'), )
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    count = db.Column(db.Integer)
    test_id = db.Column(db.Integer, db.ForeignKey('Test.id'), nullable=False)

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "test_questions_id": self.id,
            "topic_id": self.topic_id,
            "count": self.count,
            "test_id": self.test_id
        }

    def get_questions(self) -> list:
        topic = Topic.query.filter_by(id=self.topic_id).first()
        return random.sample(
            topic.questions_open + topic.questions_tf + topic.questions_multi,
            self.count)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    subjects = db.relationship('Subject', cascade='all')
    tests = db.relationship('Test', cascade='all')

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "user_id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "subjects":
            [subject.get_parameters() for subject in self.subjects],
            "tests": [test.get_parameters() for test in self.tests]
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
