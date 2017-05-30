from akamodel.model import Model
from pydal import DAL


class Person(Model):
    class Meta:
        database = DAL(('mysql://root:@127.0.0.1/hehe'), )


print(Person.columns())
