from .app import db


class Subject(db.Model):
    __tablename__ = 'Subject'
    # Define columns for the Subject table
    # subject_id = db.Column(db.Integer, primary_key=True)    # name is now the PK
    name = db.Column(db.String(100), nullable=False, primary_key=True)


class Topic(db.Model):
    __tablename__ = 'Topic'
    # topic_id = db.Column(db.Integer, primary_key=True)  # name and subject is now the PK
    name = db.Column(db.String(100), nullable=False, primary_key=True)
    subject = db.relationship('Subject')


class Variable(db.Model):
    __tablename__ = 'Variable'
    id = db.Column(db.Integer, primary_key=True)
    values = db.Column(db.String(2000), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)


class QuestionOpen(db.Model):
    __tablename__ = 'QuestionOpen'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    topic = db.relationship('Topic', uselist=False)
    variables = db.relationship('Variable')


class QuestionTF(db.Model):
    __tablename__ = 'QuestionTF'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    expression = db.Column(db.String(1000), nullable=False)
    topic = db.relationship('Topic', uselist=False)
    variables = db.relationship('Variable')


class QuestionMulti(db.Model):
    __tablename__ = 'QuestionMulti'
    id = db.Column(db.Integer, primary_key=True)
    correct_answer = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    topic = db.relationship('Topic', uselist=False)
    variables = db.relationship('Variable')
    dummy_questions = db.relationship('DummyAnswers')


class DummyAnswers(db.Model):
    __tablename__ = 'DummyAnswers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000), nullable=False)


class Test(db.Model):
    __tablename__ = 'Test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    header = db.Column(db.String(10000), nullable=False)
    questions = db.relationship('TestQuestions')

class TestQuestions(db.Model):
    __tablename__ = 'TestQuestions'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.relationship('Topic', uselist=False)
    count = db.Column(db.Integer)
