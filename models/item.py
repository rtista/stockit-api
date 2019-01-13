# Own Imports
from . import Base

# Batteries
from time import time

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String, BLOB


class Item(Base):

    __tablename__ = 'item'

    item_id = Column('item_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False)
    warehouse_id =  Column('warehouse_id', Integer, ForeignKey('warehouse.warehouse_id'), nullable=False)
    name = Column('name', String(32), nullable=False)
    description = Column('description', BLOB(8192), nullable=True)
    barcode = Column('barcode', String(64), index=True, unique=True, nullable=True)
    available = Column('available', Integer, default=0)
    allocated = Column('allocated', Integer, default=0)
    alert = Column('alert', Integer, default=0)
    created_at = Column('created_at', Integer, default=int(time()))
