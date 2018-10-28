from sqlalchemy import Column, ForeignKey, Integer, String
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
    subject_name = Column(Integer, ForeignKey('Subject.name'), nullable=False, primary_key=True)
    subject = relationship(Subject)

class QuestionOpen(Base):
    __tablename__ = 'QuestionOpen'
    id = Column(Integer, primary_key=True)
    text = Column(String(10000), nullable=False)
    topic_name = Column(Integer, ForeignKey('Topic.name'), nullable=False)
    topic = relationship(Topic)

class QuestionTF(Base):
    __tablename__ = 'QuestionTF'
    id = Column(Integer, primary_key=True)
    text = Column(String(10000), nullable=False)
    expression = Column(String(1000), nullable=False)
    topic_name = Column(Integer, ForeignKey('Topic.name'), nullable=False)
    topic = relationship(Topic)

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
    question_id = Column(Integer, ForeignKey('QuestionMulti.id'), nullable=False)
    question = relationship(QuestionMulti)



# Create an engine that stores date in the local directory's
# QuickExam.db file
engine = create_engine('sqlite:///../QuickExam.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

############ SECCION DE INSERTS (PRUEBA) ####################

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a Subject in the Subject table
new_subject = Subject(subject_name='Math')  # al parecer no se pone el id, se autoincrementa solo
session.add(new_subject)
session.commit()

# Insert an Topic in the Topic table
new_topic = Topic(topic_name='Algebra', subject=new_subject)    # no se pasan los parametros de la FK, solo el objeto
session.add(new_topic)
session.commit()

# Insert an open question in the QuestionOpen table
new_question_open = QuestionOpen(text='2+2?', topic=new_topic)
session.add(new_question_open)
session.commit()

############ SECCION DE QUERIES (PRUEBA) ####################

# Make a query to find all Subjects in the database
session.query(Subject).all()

# Return the first Subject from all Subjects in the database
subject = session.query(Subject).first()
print(subject)  # prints subject object hex address
print(subject.subject_name)    # prints the subject_name from the subject object

# Find the first Topic whose subject field is pointing to the subject object
topic = session.query(Topic).filter(Topic.subject == subject).first()

# Retrieve one OpenQuestion whose topic field is point to the topic object
session.query(QuestionOpen).filter(QuestionOpen.topic == topic).one()
open_question = session.query(QuestionOpen).filter(QuestionOpen.topic == topic).one()   # assign query to open_question
print(open_question.text)  # prints the text from the open_question object
