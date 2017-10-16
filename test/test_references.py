# content of conftest.py
import pytest
from test.fixtures.models import Person, Pet
from akamodel.errors import RecordNotFound


@pytest.fixture(scope="module")
def records():
    p = Person.create(name='jjy', age=25)
    p2 = Person.create(name='simon', age=45)
    p.pets.create(name='pipi', age=2)
    p.pets.create(name='cola', age=1)
    p2.pets.create(name='penguin', age=1)
    yield
    Person.delete_all()
    Pet.delete_all()


def test_query(records):
    person = Person.find_by(name='jjy')
    assert sorted(list(person.pets), key=lambda p: p.name) == sorted(list(Pet.where(person_id=person.id)),
                                                                     key=lambda p: p.name)
    assert person.pets.count() == 2
