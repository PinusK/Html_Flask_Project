import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    klass = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ball = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_teacher = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    questions_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return str('<user>' + str(self.id) + ' ' + self.surname + ' ' + self.name)

    def set_password(self, password):
        self.hashed_password = password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
