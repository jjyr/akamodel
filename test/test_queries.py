# content of conftest.py
import pytest
from test.fixtures.models import Person
from akamodel.errors import RecordNotFound


@pytest.fixture(scope="module")
def persons():
    Person.create(name='jjy', age=25)
    Person.create(name='Hari Seldon', age=60)
    Person.create(name='Anders', age=80)
    Person.create(name='Henry', age=30)
    Person.create(name='Henry', age=27)
    yield
    Person.delete_all()


def test_find(persons):
    p = Person.where(name='jjy').first()
    assert p == Person.find(p.id)
    assert p.age == 25
    with pytest.raises(RecordNotFound):
        Person.find(0)


def test_find_by(persons):
    p = Person.where(name='jjy').first()
    assert p == Person.find_by(age=p.age)
    with pytest.raises(RecordNotFound):
        Person.find_by(name='A girl has no name')


def test_where_chain(persons):
    assert Person.where(name='A girl has no name').first() is None
    henrys = Person.where(name='Henry')
    assert len(list(henrys)) == 2
    assert list(henrys.where(age=30)) == list(Person.where(name='Henry', age=30))
    assert list(henrys.where(age=27)) == list(Person.where(name='Henry', age=27))
    with pytest.raises(RecordNotFound):
        henrys.find_by(age=42)
    for p in Person.all():
        assert Person.where('name=:name and age=:age', name=p.name, age=p.age).first() == p


def test_where_in(persons):
    assert sorted(list(Person.where('age IN :ages', ages=(30, 80))), key=lambda p: p.name) == sorted(
        [p for p in Person.all() if p.age in [30, 80]], key=lambda p: p.name)
    assert sorted(list(Person.where('name NOT IN :names', names=('Hari Seldon', 'jjy'))),
                  key=lambda p: p.name) == sorted(
        [p for p in Person.all() if p.name not in ('Hari Seldon', 'jjy')], key=lambda p: p.name)


def test_order(persons):
    assert Person.order('age', asc=True).records() == sorted(Person.all(), key=lambda p: p.age)
    assert Person.order('age', desc=True).records() == sorted(Person.all(), key=lambda p: -p.age)


def test_limit_and_offset(persons):
    assert len(list(Person.limit(2))) == 2
    assert len(list(Person.offset(4).limit(2))) == 1
    records = Person.order('age').offset(1).limit(2).records()
    assert len(records) == 2
    assert records[0].name == 'Henry'
    assert records[1].name == 'Henry'


def test_count(persons):
    assert Person.count() == len(Person.records())
    assert Person.where(name='Henry').count() == 2


def test_group(persons):
    import itertools
    assert sorted(Person.group('name').count()) == sorted([(name, len(list(group))) for (name, group) in
                                                           itertools.groupby(Person.all(), key=lambda p: p.name)])
    assert Person.group('name').having('count(*) > 1').count() == [('Henry', 2)]
    assert ('Henry', 2) not in Person.group('name').having('count(*) = :x', x=1).count()
