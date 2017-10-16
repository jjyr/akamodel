from sqlalchemy import MetaData as RawMetaData


class MetaData(object):
    def __init__(self, raw_metadata=None):
        self._model_dict = dict()
        self._raw_metadata = raw_metadata or RawMetaData()

    def register(self, model):
        self._model_dict[model.__name__] = model

    def get_model_by_name(self, name):
        return self._model_dict[name]
