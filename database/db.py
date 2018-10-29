from sqlalchemy import Column, ForeignKey, Integer, String, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define database tables


class Subject(Base):
    __tablename__ = 'Subject'
    # Define columns for the Subject table
    # subject_id = Column(Integer, primary_key=True)    # name is now the PK
    name = Column(String(100), nullable=False, primary_key=True)


class Topic(Base):
    __tablename__ = 'Topic'
    # topic_id = Column(Integer, primary_key=True)  # name and subject is now the PK
    name = Column(String(100), nullable=False, primary_key=True)
    subject_name = Column(
        Integer, ForeignKey('Subject.name'), nullable=False, primary_key=True)
    subject = relationship(Subject)


class Variable(Base):
    __tablename__ = 'Variable'
    id = Column(Integer, primary_key=True)
    values = Column(String(2000), nullable=False)
    symbol = Column(String(50), nullable=False)
    type = Column(String(10), nullable=False)


class QuestionOpen(Base):
    __tablename__ = 'QuestionOpen'
    id = Column(Integer, primary_key=True)
    text = Column(String(10000), nullable=False)
    topic_name = Column(Integer, ForeignKey('Topic.name'), nullable=False)
    topic = relationship(Topic)


class VariableQuestionOpen(Base):
    __tablename__ = 'VariableQuestionOpen'
    question_id = Column(Integer, ForeignKey('QuestionOpen.id'), primary_key=True)
    variable_id = Column(Integer, ForeignKey('Variable.id'), primary_key=True)
    question = relationship(QuestionOpen, backref='questions_open')
    variable = relationship(Variable, backref='variables')


class QuestionTF(Base):
    __tablename__ = 'QuestionTF'
    id = Column(Integer, primary_key=True)
    text = Column(String(10000), nullable=False)
    expression = Column(String(1000), nullable=False)
    topic_name = Column(Integer, ForeignKey('Topic.name'), nullable=False)
    topic = relationship(Topic)


class VariableQuestionTF(Base):
    __tablename__ = 'VariableQuestionTF'
    question_id = Column(Integer, ForeignKey('QuestionTF.id'), primary_key=True)
    variable_id = Column(Integer, ForeignKey('Variable.id'), primary_key=True)
    question = relationship(QuestionTF, backref='questions_tf')
    variable = relationship(Variable, backref='variables')


class QuestionMulti(Base):
    __tablename__ = 'QuestionMulti'
    id = Column(Integer, primary_key=True)
    correct_answer = Column(String(1000), nullable=False)
    text = Column(String(10000), nullable=False)
    topic_name = Column(Integer, ForeignKey('Topic.name'), nullable=False)
    topic = relationship(Topic)


class DummyAnswers(Base):
    __tablename__ = 'DummyAnswers'
    id = Column(Integer, primary_key=True)
    answer = Column(String(1000), nullable=False)
    question_id = Column(
        Integer, ForeignKey('QuestionMulti.id'), nullable=False)
    question = relationship(QuestionMulti)


class Test(Base):
    __tablename__ = 'Test'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    header = Column(String(10000), nullable=False)
    topic_name = Column(
        String(100), ForeignKey('TestQuestions.topic_name'), nullable=False)
    subject_name = Column(
        String(100), ForeignKey('TestQuestions.subject_name'), nullable=False)


class TestQuestions(Base):
    __tablename__ = 'TestQuestions'
    test_id = Column(Integer, primary_key=True)
    topic_name = Column(String(100), primary_key=True)
    subject_name = Column(String(100), primary_key=True)
    count = Column(Integer, nullable=False)
    test = relationship(Test)
    topic = relationship(Topic)

    __table_args__ = (ForeignKeyConstraint([topic_name, subject_name],
                                           [Topic.name, Topic.name]),
                      ForeignKeyConstraint([test_id], [Test.id]))
