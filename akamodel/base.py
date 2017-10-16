"""
Model
"""
from akamodel.core import Core
from akamodel.schema import Schema
from akamodel.query import Query
from akamodel.persistence import Persistence
from akamodel.attribute import Attribute


class Base(Core, Schema, Query, Persistence, Attribute):
    @classmethod
    def primary_key(cls):
        return cls._get_meta_config('primary_key') or 'id'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls.abstract():
            cls.metadata().register(cls)

    def __repr__(self):
        return "<{} record {}>".format(self.__class__.__name__,
                                       {c: getattr(self, c, None) for c in self.column_names()})
