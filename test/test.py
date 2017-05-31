from akamodel.model import Model
from sqlalchemy import create_engine, MetaData

metadata = MetaData()

db = create_engine('mysql+pymysql://root:@127.0.0.1/hehe')


class Person(Model):
    class Meta:
        engine = db
        metadata = metadata


print(Person.columns())
print(Person.column_names())

new = Person.create(name='zero', age=20)
assert Person.find(new.id) == new
old_id = new.id
old_age = new.age
new.age = 21
new.save()
assert new.id == old_id
assert new.age != old_age
print("......new")
print(new)

print(Person.records())

print(Person.where(name='jjy', age=15).records())
print(Person.where(name='jjy', age=16).records())

print('.......delete all')

Person.delete_all()

print(Person.records())
