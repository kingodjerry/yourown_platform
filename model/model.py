from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.orm import sessionmaker
import flask_login
from config import Config

# Flask SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

# 데이터베이스 엔진 생성
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Session 클래스 생성
Session = sessionmaker(bind=engine)

class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'users'
    UserID = Column(Integer, primary_key=True)
    ID = Column(String(11))
    Username = Column(String(255))
    Password = Column(String(255))
    Email = Column(String(255))
    Phone = Column(String(20))
    DateOfBirth = Column(Date)
    DateJoined = Column(DateTime)
    LastLogin = Column(DateTime)
    Status = Column(Enum('active', 'inactive', name='user_status'))

    def get_id(self):
        return self.ID
