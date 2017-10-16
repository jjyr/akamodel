import akamodel as models


class BaseRecord(models.Base):
    class Meta:
        abstract = True
        engine = 2  # sqlalchemy. database or connection? or connection pool?
        metadata = 2
        table_name = ''


class Topic(BaseRecord):
    user = models.belongs_to('User')
    tags = models.has_many_and_belongs_to('Tag')


class User(BaseRecord):
    topics = models.has_many('Topic')


users = User.where().where().limit().all()
u = users.first()
topics = u.topics.all()
user = Topic.first().user
User.create(name='222')
u.update()
u.save()
u.delete()
User.first()
# transaction
# migration


#############
# 1. register models
# 2. init connection
# 3. init models structure from db
# 4. Done!
#############
