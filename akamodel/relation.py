"""
Relation present a query,
when you invoke query methods, it return a relation object instead direct sql or query results.
So akamodel can easily support query chain.

Record.where() => <# Relation>
r.all() => <# list>
r.first() => <# object>

Relation object build a real sql and execute it...
"""
from copy import copy


class Relation(object):
    def __init__(self, model):
        self._model = model
        self._table = model.table()
        self.where_clause = []
        self.select_clause = []

    def exec_sql(self, sql_exp):
        return self._model.engine().execute(sql_exp)

    def records(self):
        """
        execute sql
        :return:
        """
        rows = self.exec_sql(self.build_sql_exp('select')).fetchall()
        results = []
        column_names = self._model.column_names()
        for r in rows:
            results.append(self._model(**{c: getattr(r, c, None) for c in column_names}))
        return results

    def exists(self):
        return self.exec_sql(self.build_sql_exp('exists')).scalar()

    def all(self):
        return self.records()

    def where(self, *args, **kwargs):
        """
        User.where(name = 'joe', age = '15')
        User.where(name = 'joe').where(age = '15')
        User.where("name in ?", ['joe', 'harry', 'lee'])
        :param kwargs:
        :return:
        """
        new = copy(self)
        if kwargs:
            conditions = []
            for k, v in kwargs.items():
                conditions.append(self._table.c[k] == v)
            new.where_clause += conditions
        return new

    def select(self, *fields):
        new = copy(self)
        new.select_clause += fields
        return new

    def insert(self, **values):
        return self.exec_sql(self._table.insert().values(**values).return_defaults())

    def update_all(self, **values):
        return self.exec_sql(self.build_sql_exp('update').values(**values)).rowcount

    def delete_all(self):
        return self.exec_sql(self.build_sql_exp('delete')).rowcount

    def build_sql_exp(self, stmt):
        from sqlalchemy import exists
        exp = self._table
        if stmt == 'exists':
            exp = exp.select(exists())
        elif stmt == 'select':
            exp = exp.select()
        elif stmt == 'update':
            exp = exp.update()
        elif stmt == 'delete':
            exp = exp.delete()
        else:
            raise ValueError('unknown stmt `{}`'.format(stmt))
        for cond in self.where_clause:
            exp = exp.where(cond)
        return exp
