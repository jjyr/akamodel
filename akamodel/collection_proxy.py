class CollectionProxy(object):
    def __init__(self, model, relation=None):
        self._model = model
        self._relation = relation or model.all()

    def create(self, **values):
        attributes = self.__attributes_from_relation()
        attributes.update(values)
        return self._model.create(**attributes)

    def build(self, **values):
        attributes = self.__attributes_from_relation()
        attributes.update(values)
        return self._model(**attributes)

    def __attributes_from_relation(self):
        return self._relation.conditions()

    def __iter__(self):
        return self._relation.__iter__()

    def __getattr__(self, item):
        if hasattr(self._relation, item):
            return getattr(self._relation, item)
        raise AttributeError
