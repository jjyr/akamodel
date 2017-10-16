"""
handle queries: where, limit, order...
"""
from .collection_proxy import CollectionProxy
from .errors import RecordNotFound


class _Meta(type):
    def __getattr__(cls, item):
        proxy = cls.all()
        if hasattr(proxy, item):
            return getattr(proxy, item)
        raise AttributeError


class Query(object, metaclass=_Meta):
    @classmethod
    def all(cls):
        return CollectionProxy(model=cls)

    @classmethod
    def find(cls, id_):
        return cls.find_by(id=id_)

    @classmethod
    def find_by(cls, **kwargs):
        record = cls.where(**kwargs).first()
        if record is None:
            raise RecordNotFound('conditions: {}'.format(kwargs))
        return record
