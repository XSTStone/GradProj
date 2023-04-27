from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from static.config import DB_URI
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())

# engine = create_engine(DB_URI)
# Base = declarative_base()
# session = sessionmaker(engine)()
#
# class Student(Base):
#     __tablename__ = 'student'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     age = Column(Integer)
#     sex = Column(String(10))
#
#
# Base.metadata.create_all(engine, checkfirst=True)
#
#
# student = Student(name='Tony', age=18, sex='male')
# session.add(student)
# session.commit()