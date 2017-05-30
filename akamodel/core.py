"""
make a class become akamodel

support reflection from database
query via where, limit.. methods
"""


class RawCore(object):
    """
    sqlalchemy operations
    """
    @classmethod
    def _table_schema_from_database(cls, table_name, metadata, engine):
        from sqlalchemy import Table
        return Table(table_name, metadata, autoload=True, autoload_with=engine)


class Core(RawCore):
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
        get metadata, it supposed as a sqlalchemy metadata object
        :return:
        """
        metadata = cls._get_meta_config('metadata')
        if not metadata:
            raise ValueError("Must set Meta.metadata in model")
        return metadata
