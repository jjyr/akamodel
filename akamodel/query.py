"""
handle queries: where, limit, order...
"""

from .relation import Relation


class Query(object):
    @classmethod
    def relation(cls):
        return Relation(cls)

    # delegate methods to Relation
    for m in ['select', 'where', 'records', 'all', 'exists', 'delete_all', 'update_all', 'distinct']:
        exec ("""
@classmethod
def {method}(cls, *args, **kwargs):
    return cls.relation().{method}(*args, **kwargs)
        """.format(method=m))

    @classmethod
    def find(cls, id_):
        return cls.find_by(id=id_)

    @classmethod
    def find_by(cls, **kwargs):
        return cls.where(**kwargs).first()
