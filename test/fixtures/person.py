from akamodel.model import Model
from .database import metadata, db

from sqlalchemy import Table, Column, Integer, String

Table('person', metadata,
      Column('id', Integer, primary_key=True, autoincrement='auto'),
      Column('name', String(16), nullable=False),
      Column('age', Integer)
      ).create(db)


class Person(Model):
    class Meta:
        engine = db
        metadata = metadata
