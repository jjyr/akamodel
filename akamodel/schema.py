"""
load model schema from db
"""

from akamodel.utils.quoting import *


class Schema(object):
    __schema_loaded = False

    @classmethod
    def __load_schema(cls):
        """
        load and define columns
        :return:
        """
        if cls.__is_schema_loaded():
            return
        cls.__force_load_schema()

    @classmethod
    def __force_load_schema(cls):
        cls._table = cls._table_schema_from_database(cls.table_name(), cls.metadata(), cls.engine())
        cls.__schema_loaded = True

    @classmethod
    def __is_schema_loaded(cls):
        return cls.__schema_loaded

    @classmethod
    def table(cls):
        cls.__load_schema()
        return cls._table

    @classmethod
    def columns(cls):
        return cls.table().columns

    @classmethod
    def column_names(cls):
        return [c.name for c in cls.columns()]

    @classmethod
    def table_name(cls):
        return cls._get_meta_config('table_name') or cls.__name__.lower()

    @classmethod
    def quoted_table_name(cls):
        return quote_table_name(cls.table_name())
