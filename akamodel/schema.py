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
        database = cls.get_database()
        cls.__columns = database.executesql(
            'select * from information_schema.columns where table_name="{}"'.format(cls.table_name()),
            as_dict=True)
        cls.__load_schema = True

    @classmethod
    def __is_schema_loaded(cls):
        return cls.__schema_loaded

    @classmethod
    def columns(cls):
        cls.__load_schema()
        return cls.__columns

    @classmethod
    def column_names(cls):
        pass

    @classmethod
    def is_table_exists(cls):
        pass

    @classmethod
    def table_name(cls):
        return cls._get_metadata('table_name') or cls.__name__.lower()

    @classmethod
    def quoted_table_name(cls):
        return quote_table_name(cls.table_name())
