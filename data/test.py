import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Test(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'test'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    a_task_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')
