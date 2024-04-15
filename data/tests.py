import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "tests"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    test_word = sqlalchemy.Column(sqlalchemy.String)
    test_sign = sqlalchemy.Column(sqlalchemy.String)
    test_completed = sqlalchemy.Column(sqlalchemy.Boolean)
