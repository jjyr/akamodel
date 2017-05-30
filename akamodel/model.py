"""
Model
"""
from akamodel.core import Core
from akamodel.schema import Schema
from akamodel.query import Query
from akamodel.persistence import Persistence
from akamodel.attribute import Attribute


class Model(Core, Schema, Query, Persistence, Attribute):
    def __repr__(self):
        return "<{} record {}>".format(self.__class__.__name__,
                                       {c: getattr(self, c, None) for c in self.column_names()})
