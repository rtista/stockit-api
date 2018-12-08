# Own Imports
from . import Base

# Batteries
from time import time

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String


class User(Base):

    __tablename__ = 'user'

    user_id = Column('user_id', Integer, primary_key=True)
    account_id = Column('account_id', Integer, ForeignKey("account.account_id"), nullable=False)
    username = Column('username', String(16), unique=True, index=True, nullable=False)
    email = Column('email', String(64), unique=True, nullable=False)
    password = Column('password', String(100), nullable=False)
    created_at = Column('created_at', Integer, default=int(time()))