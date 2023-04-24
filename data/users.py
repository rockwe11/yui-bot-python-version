import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    did = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    vid = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    bonustm = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=True)
    coins = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=True)
    language = sqlalchemy.Column(sqlalchemy.CHAR)
