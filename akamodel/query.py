"""
handle queries: where, limit, order...
"""
from .collection_proxy import CollectionProxy


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

