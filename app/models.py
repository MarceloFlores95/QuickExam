from .app import db
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

    def get_parameters(self):
        return {"id":self.id, "name":self.name, "user_id":self.user_id}


class Topic(db.Model):
    __tablename__ = 'Topic'
    __table_args__ = (
        db.UniqueConstraint('name', 'subject_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(
        db.Integer, db.ForeignKey('Subject.id'), nullable=False)
    questions_open = db.relationship('QuestionOpen', cascade='all')
    questions_tf = db.relationship('QuestionTF', cascade='all')
    questions_multi = db.relationship('QuestionMulti', cascade='all')
    test_questions = db.relationship('TestQuestions', cascade='all')

    def get_parameters(self):
        return {"id":self.id, "name":self.name, "subject_id":self.subject_id}


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


class QuestionOpen(db.Model):
    __tablename__ = 'QuestionOpen'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')


class QuestionTF(db.Model):
    __tablename__ = 'QuestionTF'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000), nullable=False)
    expression = db.Column(db.String(1000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')


class QuestionMulti(db.Model):
    __tablename__ = 'QuestionMulti'
    id = db.Column(db.Integer, primary_key=True)
    correct_answer = db.Column(db.String(1000), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    variables = db.relationship('Variable', cascade='all')
    dummy_questions = db.relationship('DummyAnswers', cascade='all')


class DummyAnswers(db.Model):
    __tablename__ = 'DummyAnswers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(1000), nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey('QuestionMulti.id'), nullable=False)


class Test(db.Model):
    __tablename__ = 'Test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    header = db.Column(db.String(10000), nullable=False)
    questions = db.relationship('TestQuestions', cascade='all')
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


class TestQuestions(db.Model):
    __tablename__ = 'TestQuestions'
    __table_args__ = (
        db.UniqueConstraint('topic', 'test_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Integer, db.ForeignKey('Topic.id'), nullable=False)
    count = db.Column(db.Integer)
    test_id = db.Column(db.Integer, db.ForeignKey('Test.id'), nullable=False)
