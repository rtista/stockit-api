# Own Imports
from . import Base

# Batteries
from time import time

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String


class Item(Base):

    __tablename__ = 'item'

    item_id = Column('item_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False)
    warehouse_id =  Column('warehouse_id', Integer, ForeignKey('warehouse.warehouse_id'), nullable=False)
    name = Column('name', String(32), nullable=False)
    description = Column('description', String(256), nullable=True)
    quantity = Column('quantity', Integer, default=0)
    barcode = Column('barcode', String(64), index=True, nullable=True)
    section = Column('section', String(32), nullable=True)
    created_at = Column('created_at', Integer, default=int(time()))
