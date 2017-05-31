# content of conftest.py
import pytest
from ..fixtures.person import Person


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


def test_find_by(persons):
    p = Person.where(name='jjy').first()
    assert p == Person.find_by(age=p.age)
    assert Person.find_by(name='A girl has no name') is None


def test_where_chain(persons):
    henrys = Person.where(name='Henry')
    assert len(list(henrys)) == 2
    assert henrys.where(age=30).all() == Person.where(name='Henry', age=30).all()
