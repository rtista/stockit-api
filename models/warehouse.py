# Own Imports
from . import Base

# Batteries
from time import time

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Enum


class Warehouse(Base):

    __tablename__ = 'warehouse'

    warehouse_id = Column('warehouse_id', Integer, primary_key=True)
    name = Column('name', String(32), nullable=False)
    description = Column('description', String(256), nullable=True)
    latitude = Column('latitude', Float, nullable=True)
    longitude = Column('longitude', Float, nullable=True)
    created_at = Column('created_at', Integer, default=int(time()))

class UserWarehouse(Base):

    __tablename__ = 'user_warehouse'

    warehouse_id =  Column('warehouse_id', Integer, ForeignKey('warehouse.warehouse_id'), primary_key=True, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id'), nullable=False)
    permission = Column('permission', Enum('r', 'rw'), nullable=False)



