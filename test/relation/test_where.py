# content of conftest.py
import pytest
from ..fixtures.person import Person
from akamodel.errors import RecordNotFound


@pytest.fixture(scope="module")
def persons():
    Person.create(name='jjy', age=25)
    Person.create(name='Hari Seldon', age=60)
    Person.create(name='Alanjandro', age=80)
    Person.create(name='Henry', age=30)
    Person.create(name='Henry', age=27)


def test_find(persons):
    p = Person.where(name='jjy').first()
    assert p == Person.find(p.id)
    assert p.age == 25
    with pytest.raises(RecordNotFound):
        Person.find(42)


def test_find_by(persons):
    p = Person.where(name='jjy').first()
    assert p == Person.find_by(age=p.age)
    with pytest.raises(RecordNotFound):
        Person.find_by(name='A girl has no name')


def test_where_chain(persons):
    assert Person.where(name='A girl has no name').first() is None
    henrys = Person.where(name='Henry')
    assert len(list(henrys)) == 2
    assert henrys.where(age=30).all() == Person.where(name='Henry', age=30).all()
