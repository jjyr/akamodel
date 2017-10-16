"""
make a class become akamodel

support reflection from database
query via where, limit.. methods
"""
from akamodel.metadata import MetaData


class RawCore(object):
    """
    sqlalchemy operations
    """

    @classmethod
    def _table_schema_from_database(cls):
        from sqlalchemy import Table
        table_name = cls.table_name()
        raw_metadata = cls.metadata()._raw_metadata
        engine = cls.engine()
        return Table(table_name, raw_metadata, autoload=True, autoload_with=engine)


class Core(RawCore):
    __metadata = MetaData()

    @classmethod
    def _meta(cls):
        return getattr(cls, 'Meta')

    @classmethod
    def _get_meta_config(cls, key):
        return getattr(cls._meta(), key, None)

    @classmethod
    def engine(cls):
        """
        get engine, it supposed as a sqlalchemy engine object
        :return:
        """
        engine = cls._get_meta_config('engine')
        if not engine:
            raise ValueError("Must set Meta.engine in model")
        return engine

    @classmethod
    def metadata(cls):
        """
        get metadata
        :return:
        """
        metadata = cls._get_meta_config('metadata') or cls.__metadata
        if not metadata:
            raise ValueError("Must set Meta.metadata in model")
        return metadata

    @classmethod
    def abstract(cls):
        """
        is this model abstract
        :return:
        """
        return cls._get_meta_config('abstract') or False
