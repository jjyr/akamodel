from akamodel.base import Base
from .database import metadata, db

from sqlalchemy import Table, Column, Integer, String

Table('person', metadata,
      Column('id', Integer, primary_key=True, autoincrement='auto'),
      Column('name', String(16), nullable=False),
      Column('age', Integer)
      ).create(db, checkfirst=True)


class Person(Base):
    class Meta:
        engine = db
        metadata = metadata
