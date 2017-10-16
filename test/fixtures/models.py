from akamodel import Base
from akamodel.reference import has_many
from .database import metadata, db

from sqlalchemy import Table, Column, Integer, String

Table('person', metadata,
      Column('id', Integer, primary_key=True, autoincrement='auto'),
      Column('name', String(16), nullable=False),
      Column('age', Integer)
      ).create(db, checkfirst=True)

Table('pet', metadata,
      Column('id', Integer, primary_key=True, autoincrement='auto'),
      Column('person_id', Integer),
      Column('name', String(16), nullable=False),
      Column('age', Integer)
      ).create(db, checkfirst=True)


class BaseRecord(Base):
    class Meta:
        engine = db
        abstract = True


class Person(BaseRecord):
    pets = has_many('Pet')


class Pet(BaseRecord):
    pass
