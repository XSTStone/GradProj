from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from flask_login import UserMixin
from werkzeug.security import check_password_hash

Base = declarative_base()


class User(Base):
    """数据库_User类"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password = Column(String(50))


class User_Session(UserMixin):
    """登陆_User类"""
    def __init__(self, user):
        self.username = user.get_username()
        self.password_hash = user.get_password()
        self.id = user.get_id()

    def verify_password(self, password):
        """密码验证"""
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """获取用户ID"""
        return self.id

    @staticmethod
    def get(user_id):
        """根据用户ID获取User Entity，为login_user提供支持"""
        if not user_id:
            return None
        found_user = Users_db.query.filter(Users_db.id == user_id).first()
        if found_user:
            return found_user
        else:
            return None