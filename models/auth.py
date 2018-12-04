# Own Imports
from . import Base
from config import AppConfig

# Batteries
from time import time
from enum import Enum

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from secrets import token_hex


class AuthToken(Base):

    __tablename__ = 'auth_token'

    user_id = Column('user_id', Integer, ForeignKey("user.user_id"), primary_key=True, nullable=False)
    auth_type = Column('auth_type', Enum('bearer'), unique=True, nullable=False)
    token = Column('token', String(32), unique=True, nullable=False)
    expires_at = Column('expires_at', Integer, default=int(time() + AppConfig.TOKEN_LIFE))