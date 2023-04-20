import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class GuildSettings(SqlAlchemyBase):
    __tablename__ = 'guild_settings'

    guildid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    prefix = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    language = sqlalchemy.Column(sqlalchemy.CHAR, nullable=True)
