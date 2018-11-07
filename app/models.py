from .app import db
from .pdf import PDF
from typing import Dict, Union
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    subjects = db.relationship('Subject', cascade='all')
    tests = db.relationship('Test', cascade='all')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Subject(db.Model):
    __tablename__ = 'Subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    topics = db.relationship('Topic', cascade='all')
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def get_parameters(self) -> Dict[str, Union[str, int]]:
        return {"id": self.id, "name": self.name}


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

    def get_parameters(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.id,
            "name": self.name,
            "subject_id": self.subject_id
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
            "id": self.id,
            "values": self.values,
            "symbol": self.symbol,
            "type": self.type,
            "question_open_id": self.question_open_id,
            "question_tf_id": self.question_tf_id,
            "question_multi_id": self.question_multi_id
        }


class QuestionOpen(db.Model):
    __tablename__ = 'QuestionOpen'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')

    def get_parameters(self) -> Dict[str, Union[str, int]]:
        return {"id": self.id, "text": self.text, "topic_id": self.topic_id}


class QuestionTF(db.Model):
    __tablename__ = 'QuestionTF'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    expression = db.Column(db.String(1000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')

    def get_parameters(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.id,
            "text": self.text,
            "expression": self.expression,
            "topic_id": self.topic_id
        }


class QuestionMulti(db.Model):
    __tablename__ = 'QuestionMulti'
    id = db.Column(db.Integer, primary_key=True)
    correct_answer = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')
    dummy_questions = db.relationship('DummyAnswers', cascade='all')

    def get_parameters(self) -> Dict[str, Union[str, int]]:
        dummies = DummyAnswers.query.filter_by(question_id=self.id)
        return {
            "id": self.id,
            "correct_answer": self.correct_answer,
            "text": self.text,
            "topic_id": self.topic_id,
            "dummies": [dummy.get_parameters() for dummy in dummies]
        }


class DummyAnswers(db.Model):
    __tablename__ = 'DummyAnswers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000), nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey('QuestionMulti.id'), nullable=False)

    def get_parameters(self) -> Dict[str, Union[str, int]]:
        return {"id": self.id, "answer": self.answer}


class Test(db.Model):
    __tablename__ = 'Test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    header = db.Column(db.String(10000), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    questions = db.relationship('TestQuestions', cascade='all')
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def get_parameters(self) -> Dict[str, Union[str, int]]:
        questions = TestQuestions.query.filter_by(test_id=self.id)
        return {
            "id": self.id,
            "name": self.name,
            "header": self.header,
            "questions": [question.get_parameters() for question in questions]
        }


class TestQuestions(db.Model):
    __tablename__ = 'TestQuestions'
    __table_args__ = (db.UniqueConstraint('topic_id', 'test_id'), )
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    count = db.Column(db.Integer)
    test_id = db.Column(db.Integer, db.ForeignKey('Test.id'), nullable=False)

    def get_parameters(self):
        return {"id": self.id, "topic_id": self.topic_id, "count": self.count}
