# content of conftest.py
import pytest
from test.fixtures.models import Person
from akamodel.errors import RecordNotFound


@pytest.fixture(scope="module")
def records():
    Person.create(name='jjy', age=25)
    Person.create(name='Hari Seldon', age=60)
    Person.create(name='Anders', age=80)
    Person.create(name='Henry', age=30)
    Person.create(name='Henry', age=27)
    yield
    Person.delete_all()


def test_build(records):
    p = Person.where(name='jjy', age=25).build()
    p2 = Person.where(name='jjy').where(age=25).build()
    assert p.is_new_record()
    assert p.age == 25 and p.name == 'jjy'
    assert p == p2


def test_first_or_build(records):
    p = Person.where(name='jjy', age=25).first_or_build()
    p2 = Person.where(name='jjy', age=35).first_or_build()
    assert not p.is_new_record()
    assert p2.is_new_record()


def test_first_or_create(records):
    p = Person.where(name='jjy', age=25).first_or_create()
    p2 = Person.where(name='jjy', age=35).first_or_create()
    assert not p.is_new_record()
    assert not p2.is_new_record() and p2.name == 'jjy' and p2.age == 35
