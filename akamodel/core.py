"""
make a class become akamodel

support reflection from database
query via where, limit.. methods
"""


class Core(object):
    @classmethod
    def _get_meta(cls):
        return getattr(cls, 'Meta')

    @classmethod
    def _get_metadata(cls, key):
        return getattr(cls._get_meta(), key, None)

    @classmethod
    def get_database(cls):
        """
        get database, it supposed as a sqlalchemy engine object
        :return:
        """
        database = cls._get_metadata('database')
        if not database:
            raise ValueError("Must set Meta.database in model")
        return database
