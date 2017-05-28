"""
Relation present a query,
when you invoke query methods, it return a relation object instead direct sql or query results.
So akamodel can easily support query chain.

Record.where() => <# Relation>
r.all() => <# list>
r.first() => <# object>

Relation object build a real sql and execute it...
"""
from . import query


class Relation(query.Query):
    def records(self):
        """
        execute sql
        :return:
        """
        pass

    def insert(self):
        pass

    def update(self):
        pass

    def update_all(self):
        pass

    def delete(self):
        pass

    def delete_all(self):
        pass

    def to_sql(self):
        pass
