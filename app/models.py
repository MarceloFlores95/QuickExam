from .app import db


class Subject(db.Model):
    __tablename__ = 'Subject'
    # Define columns for the Subject table
    # subject_id = db.Column(db.Integer, primary_key=True)    # name is now the PK
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, primary_key=True)
    topics = db.relationship('Topic', cascade='all')


class Topic(db.Model):
    __tablename__ = 'Topic'
    # topic_id = db.Column(db.Integer, primary_key=True)  # name and subject is now the PK
    name = db.Column(db.String(100), nullable=False, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('Subject.id'), nullable=False)


class Variable(db.Model):
    __tablename__ = 'Variable'
    id = db.Column(db.Integer, primary_key=True)
    values = db.Column(db.String(2000), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    question_open_id = db.Column(db.Integer, db.ForeignKey('QuestionOpen.id'))
    question_tf_id = db.Column(db.Integer, db.ForeignKey('QuestionTF.id'))
    question_multi_id = db.Column(db.Integer, db.ForeignKey('QuestionMulti.id'))


class QuestionOpen(db.Model):
    __tablename__ = 'QuestionOpen'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    topic = db.relationship('Topic', uselist=False)
    variables = db.relationship('Variable', cascade='all')


class QuestionTF(db.Model):
    __tablename__ = 'QuestionTF'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    expression = db.Column(db.String(1000), nullable=False)
    topic = db.relationship('Topic', uselist=False)
    variables = db.relationship('Variable', cascade='all')


class QuestionMulti(db.Model):
    __tablename__ = 'QuestionMulti'
    id = db.Column(db.Integer, primary_key=True)
    correct_answer = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    topic = db.relationship('Topic', uselist=False)
    variables = db.relationship('Variable', cascade='all')
    dummy_questions = db.relationship('DummyAnswers', cascade='all')


class DummyAnswers(db.Model):
    __tablename__ = 'DummyAnswers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('QuestionMulti.id'), nullable=False)


class Test(db.Model):
    __tablename__ = 'Test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    header = db.Column(db.String(10000), nullable=False)
    questions = db.relationship('TestQuestions', cascade='all')


class TestQuestions(db.Model):
    __tablename__ = 'TestQuestions'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.relationship('Topic', uselist=False)
    count = db.Column(db.Integer)
    test_id = db.Column(db.Integer, db.ForeignKey('Test.id'), nullable=False)
