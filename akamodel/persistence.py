class Persistence(object):
    @classmethod
    def create(cls, **values):
        new = cls(**values)
        new.save()
        return new

    def create_or_update(self):
        if self.is_new_record():
            return self._create_record()
        else:
            return self._update_record()

    def _update_record(self, attribute_names=None):
        attribute_names = attribute_names or self.__class__.column_names()
        return self.__class__.relation().where(id = self.id).update_all(
            **{a: getattr(self, a, None) for a in attribute_names})

    def _create_record(self, attribute_names=None):
        attribute_names = attribute_names or self.__class__.column_names()
        result = self.__class__.relation().insert(**{a: getattr(self, a, None) for a in attribute_names})
        id_ = result.inserted_primary_key[0]
        self.id = id_
        return id_

    def save(self):
        self.create_or_update()

    # FIXME only works on id as primary keys
    def is_new_record(self):
        return getattr(self, 'id', None) is None or not self.__class__.relation().where(id=self.id).exists()
