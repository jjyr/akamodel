"""
handle queries: where, limit, order...
"""

from .relation import Relation
from .errors import RecordNotFound


class _Meta(type):
    def __getattr__(cls, item):
        relation = cls.all()
        if hasattr(relation, item):
            return getattr(relation, item)
        raise AttributeError


class Query(object, metaclass=_Meta):
    @classmethod
    def all(cls):
        return Relation(cls)

    @classmethod
    def find(cls, id_):
        return cls.find_by(id=id_)

    @classmethod
    def find_by(cls, **kwargs):
        record = cls.where(**kwargs).first()
        if record is None:
            raise RecordNotFound('conditions: {}'.format(kwargs))
        return record
