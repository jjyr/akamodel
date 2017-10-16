from .relation import Relation


class CollectionProxy(object):
    def __init__(self, model, relation=None):
        self._model = model
        self._relation = relation or Relation(model=model)

    def create(self, **values):
        attributes = self.__attributes_from_relation()
        attributes.update(values)
        return self._model.create(**attributes)

    def build(self, **values):
        attributes = self.__attributes_from_relation()
        attributes.update(values)
        return self._model(**attributes)

    def first_or_build(self, **values):
        return self.first() or self.build(**values)

    def first_or_create(self, **values):
        return self.first() or self.create(**values)

    def where(self, *args, **kwargs):
        return CollectionProxy(model=self._model, relation=self._relation.where(*args, **kwargs))

    def __attributes_from_relation(self):
        return self._relation.conditions()

    def __iter__(self):
        return self._relation.__iter__()

    def __getattr__(self, item):
        if hasattr(self._relation, item):
            return getattr(self._relation, item)
        raise AttributeError
