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
        return self.__class__.where(id=self.id).update_all(
            **{a: getattr(self, a, None) for a in attribute_names})

    def _create_record(self, attribute_names=None):
        attribute_names = attribute_names or self.__class__.column_names()
        attribtutes = {a: getattr(self, a, None) for a in attribute_names}
        # should handle defaults columns?
        primary_key = self.__class__.primary_key()
        if primary_key in attribtutes and attribtutes[primary_key] is None:
            del attribtutes[primary_key]
        result = self.__class__.all()._insert(**attribtutes)
        id_ = result.inserted_primary_key[0]
        self.id = id_
        return id_

    def save(self):
        self.create_or_update()

    def is_new_record(self):
        primary_key = self.__class__.primary_key()
        return getattr(self, primary_key, None) is None or not self.__class__.where(
            id=self.attributes[primary_key]).exists()
