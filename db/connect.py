from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from config import DB_URI

engine = create_engine(DB_URI)
Base = declarative_base()
session = sessionmaker(engine)()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    sex = Column(String(10))


Base.metadata.create_all(engine, checkfirst=True)


student = Student(name='Tony', age=18, sex='male')
session.add(student)
session.commit()