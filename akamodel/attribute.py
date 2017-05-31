class Attribute(object):
    def __init__(self, **attributes):
        self.__dict__.update(**attributes)

    def __eq__(self, other):
        return type(self) == type(other) and self.__dict__ == other.__dict__
