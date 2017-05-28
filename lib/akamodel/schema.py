"""
load model schema from db
"""


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
        get connection
        query..
        build_attributes
        cls.__load_schema = True

    @classmethod
    def __is_schema_loaded(cls):
        return cls.__load_schema

    def columns(self):
        pass

    def column_names(self):
        pass

    def is_table_exists(self):
        pass

    def table_name(self):
        pass
