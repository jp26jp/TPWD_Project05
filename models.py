from peewee import *
from slugify import slugify

DATABASE = SqliteDatabase('my_app.db')


class Entry(Model):
    title = TextField()
    slug = TextField()
    date = DateField()
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE

    # credit: https://stackoverflow.com/a/32333011/4373927
    def __init__(self, *args, **kwargs):
        if 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)

    @classmethod
    def create_entry(cls, title, date, time_spent, learned, resources):
        with DATABASE.transaction():
            return cls.create(title=title, date=date, time_spent=time_spent, learned=learned, resources=resources)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
