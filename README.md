Akamodel
------------

An ActiveRecord-like ORM in python world

# Installation

> Note: **Akamodel** only support python3

> You maybe noticed Akamodel is not yet product-ready, I would be glad if you use it in personal projects. Feel free to open issues or contact me if you have any confuse

`pip install git+https://github.com/jjyr/akamodel.git@master`

# Development

``` bash
git clone https://github.com/jjyr/akamodel.git
cd akamodel && py.test
```

# Usage

Akamodel is built upon SQLAlchemy, before use you need install database driver libraries

Run `pip install pymysql3` to install mysql driver

You can also use PostgreSQL, Oracle, Microsoft SQL server.. [View SQLAlchemy document](http://docs.sqlalchemy.org/en/latest/dialects/index.html) to find out how to install DB drivers

## Table define
> This step is not necessary for using akamodel, akamodel can auto load DB schema from database. So it's not necessary to define table schema in python if you want to access exists tables. This section just demostrate currently solution for definition and creation of tables: using SQLAlchemy

 In the future, Akamodel will provide table define DSL to instead of directly use SQLAlchemy

 But sadly, currently we still need SQLAlchemy for table creation
``` python
from sqlalchemy import MetaData, create_engine

# Initialize SQLAlchemy MetaData for table creation
metadata = MetaData()
db = create_engine('mysql+pymysql://localhost/test')

# Define tables
Table('person', metadata,
      Column('id', Integer, primary_key=True, autoincrement='auto'),
      Column('name', String(16), nullable=False),
      Column('age', Integer)
      ).create(db, checkfirst=True)

Table('pet', metadata,
      Column('id', Integer, primary_key=True, autoincrement='auto'),
      Column('person_id', Integer),
      Column('name', String(16), nullable=False),
      Column('age', Integer)
      ).create(db, checkfirst=True)
```

## Using Akamodel

View [test cases](/test) to find out newest features

``` python
from akamodel import Base
from akamodel.reference import has_many
from sqlalchemy import create_engine

# Create SQLAlchemy engine
db = create_engine('mysql+pymysql://localhost/test')

class BaseRecord(Base):
    class Meta:
        engine = db
        abstract = False

# Mapping 'person' and 'pet' table
class Person(BaseRecord):
    pets = has_many('Pet') # Build relation on pet.person_id


class Pet(BaseRecord):
    pass


# Create records
jjy = Person.create(name='jjy', age=25)
hari = Person.create(name='Hari Seldon', age=60)
Person.count() # 2


# Basic queries
Person.find(1) == Person.find_by(id=1) == Person.where(id=1).first() # true
Person.find(0) or Person.find_by(id: 0) # find find_by raise akamodel.errors.RecordNotFound if not found
Person.where(id=0).first() # first return None if not found
Person.where(name='jjy', age=25).first() == jjy # True


# Query with params
Person.where('name=:name', name='jjy').first() == jjy
Person.where('age IN :ages', ages=(25, 60)).count() # 2


# Support query chain
Person.where(name='jjy').where(age=25).first() == jjy # True
Person.where(name='jjy').find_by(age=25) == jjy # True


# Lazy Evaluation
Person.all() # <CollectionProxy ...>
list(Person.all()) # <list ...>
Person.all().records() # <list ...>


# Advance functions
Person.order('age', desc=True)
Person.offset(1).limit(1)
Person.group('name').count() # [('jjy', 1), ('Hari Seldon', 1)]
Person.group('name').having('count(*) > 1').count() # []


# Build or create record by query condition
person = Person.where(name='jack', age=30).build() # build record from query condition, do not save to database
person.is_new_record() # True

person = Person.where(name='jack', age=30).first_or_build() # find or build record from query condition
person.is_new_record() # True

person = Person.where(name='jack', age=30).first_or_create() # find or create new record from query condition, Equivalent with Person.create(name='jack', age=30)
person.is_new_record() # False


# Model relation
cola = jjy.pets.create(name='cola', age=1) # create related pet record
cola.attributes # {'name': 'cola', age: 1, person_id: 1}
jjy.pets.first() == cola # query from pet
jjy.pets.find_by(name='cola') == cola # equivalent with Pet.where(person_id=jjy.id).find_by(name='cola')

```

# Future Plan

- [ ] Advanced relations (`has_many`, `belongs_to`, `has_and_belongs_to`, polymorphic relation)
- [ ] DB transaction
- [ ] Thread safe
- [ ] Single table inherited
- [ ] Advanced DB functions(lock, joins...)
- [ ] Advanced model features (callbacks, changes, validation)
- [ ] * Table define DSL
- [ ] * DB migration tools
