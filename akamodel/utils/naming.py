import re

__under_score_re = re.compile(r'.([A-Z])')


def to_underscore(name):
    return __under_score_re.sub(r'_\1', name).lower()
