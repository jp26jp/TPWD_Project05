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

    def get_entries(self):
        return Entry.select()

    # credit: https://stackoverflow.com/a/32333011/4373927
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)

    @classmethod
    def create_entry(cls, title, date, time_spent, learned, resources):
        try:
            with DATABASE.transaction():
                cls.create(title=title, date=date, time_spent=time_spent, learned=learned, resources=resources)
        except IntegrityError:
            raise ValueError("Title already exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
