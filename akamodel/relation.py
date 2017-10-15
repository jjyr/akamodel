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
        self._where_clause = []
        self._select_clause = []
        self._distinct_values = []
        self._order_clause = []
        self._offset = None
        self._limit = None
        self._group_values = []
        self._having_clause = []
        self._parameters = dict()

    def exec_sql(self, sql_exp):
        return self._model.engine().execute(sql_exp, self._parameters)

    def __iter__(self):
        return self.records().__iter__()

    def all(self):
        return self

    def records(self):
        """
        execute sql
        :return:
        """
        rows = self.exec_sql(self._build_sql_exp('select')).fetchall()
        results = []
        column_names = self._model.column_names()
        for r in rows:
            results.append(self._model(**{c: getattr(r, c, None) for c in column_names}))
        return results

    def exists(self):
        return self.exec_sql(self._build_sql_exp('exists')).scalar()

    def first(self):
        r = self.exec_sql(self._build_sql_exp('select')).first()
        return self._model(**{c: getattr(r, c, None) for c in self._model.column_names()}) if r else None

    def count(self, field=None):
        if len(self._group_values) == 0:
            return self.exec_sql(self._build_sql_exp('count', field)).scalar()
        else:
            return self.exec_sql(self._build_sql_exp('count', field)).fetchall()

    def where(self, *args, **kwargs):
        """
        User.where(name = 'joe', age = '15')
        User.where(name = 'joe').where(age = '15')
        User.where("name in ?", ['joe', 'harry', 'lee'])
        :param kwargs:
        :return:
        """
        new = copy(self)
        if len(args) > 0:
            new._where_clause.append(('sql_cond', args[0], kwargs))
        elif kwargs:
            conditions = []
            for k, v in kwargs.items():
                conditions.append(('kw_cond', self._table.c[k] == v))
            new._where_clause += conditions
        return new

    def distinct(self, *args):
        new = copy(self)
        new._distinct_values = args
        return new

    def select(self, *fields):
        new = copy(self)
        new._select_clause += fields
        return new

    def order(self, field, desc=False, asc=False):
        if desc is True and asc is True:
            raise ValueError('desc and asc can not be same value')
        asc = desc is False
        new = copy(self)
        new._order_clause.append((field, asc), )
        return new

    def group(self, *fields):
        new = copy(self)
        new._group_values = fields
        return new

    def having(self, *args, **kwargs):
        """
        User.where(name = 'joe', age = '15')
        User.where(name = 'joe').where(age = '15')
        User.where("name in ?", ['joe', 'harry', 'lee'])
        :param kwargs:
        :return:
        """
        new = copy(self)
        new._having_clause.append((args[0], kwargs))
        return new

    def limit(self, limit):
        new = copy(self)
        new._limit = limit
        return new

    def offset(self, offset):
        new = copy(self)
        new._offset = offset
        return new

    def _insert(self, **values):
        return self.exec_sql(self._table.insert().values(**values).return_defaults())

    def update_all(self, **values):
        return self.exec_sql(self._build_sql_exp('update').values(**values)).rowcount

    def delete_all(self):
        return self.exec_sql(self._build_sql_exp('delete')).rowcount

    def _build_sql_exp(self, stmt, *args):
        from sqlalchemy import exists, select, func
        if stmt == 'exists':
            exp = self._table.select(exists())
        elif stmt == 'count':
            query = []
            c = args[0]
            if self._group_values is not None:
                query += [self._table.c[c] for c in self._group_values]
            if c is not None:
                query.append(func.count(self._table.c[c]))
            else:
                query.append(func.count())
            exp = select(query).select_from(self._table)
        elif stmt == 'select':
            if self._distinct_values:
                exp = select([self._table.c[c] for c in self._distinct_values])
                exp = exp.distinct()
            else:
                exp = select([self._table.c[c] for c in self._select_clause] or self._table.columns)
        elif stmt == 'update':
            exp = self._table.update()
        elif stmt == 'delete':
            exp = self._table.delete()
        else:
            raise ValueError('unknown stmt `{}`'.format(stmt))
        for conds in self._where_clause:
            if conds[0] == 'sql_cond':
                exp = exp.where(conds[1])
                self._parameters.update(conds[2])
            elif conds[0] == 'kw_cond':
                exp = exp.where(conds[1])
        for order in self._order_clause:
            c, asc = order
            order_exp = self._table.c[c]
            if asc:
                order_exp = order_exp.asc()
            else:
                order_exp = order_exp.desc()
            exp = exp.order_by(order_exp)
        if len(self._group_values) > 0:
            exp = exp.group_by(*[self._table.c[c] for c in self._group_values])
        for cond, parameter in self._having_clause:
            exp = exp.having(cond)
            if len(parameter) > 0:
                self._parameters.update(parameter)
        if self._offset:
            exp = exp.offset(self._offset)
        if self._limit:
            exp = exp.limit(self._limit)
        return exp
