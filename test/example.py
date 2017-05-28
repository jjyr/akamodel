from akamodel import Model


class BaseModel(Model):
    class Meta:
        abstract = True
        database = 2 # sqlalchemy. database or connection? or connection pool?
        tablename = ''


class User(BaseModel):
    topics = has_many('Topic')


users = User.where().where().limit().all()
topics = u.topics().all()
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
