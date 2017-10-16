from akamodel.utils import naming


class Reference(object):
    def __init__(self, ref_class_name):
        self._ref_class_name = ref_class_name

    def __get__(self, record, record_cls):
        return self.query_result(record, record_cls, record_cls.metadata())

    def query_result(self, record, record_cls):
        raise NotImplementedError

    # to_ref_column convert Reference -> 'reference_id'
    def to_ref_column(self, record_cls):
        cls_name = record_cls.__name__
        return "{table}_{id}".format(table=naming.to_underscore(cls_name), id=record_cls.primary_key())

    def ref_scope(self, metadata):
        ref_class = metadata.get_model_by_name(self._ref_class_name)
        return ref_class.all()


class HasManyReference(Reference):
    def query_result(self, record, record_cls, metadata):
        ref_column = self.to_ref_column(record_cls)
        primary_key_value = record.attributes[record_cls.primary_key()]
        return self.ref_scope(metadata).where(**{ref_column: primary_key_value})


has_many = HasManyReference
