# Own Imports
from . import Base

# Batteries
from time import time

# Third Party Imports
from sqlalchemy import Column, Integer, String

class Account(Base):

    __tablename__ = 'account'

    account_id = Column('account_id', Integer, primary_key=True)
    name = Column('name', String(16), nullable=False)
    created_at = Column('created_at', Integer, default=int(time()))