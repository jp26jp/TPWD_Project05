from peewee import *

DATABASE = SqliteDatabase('my_app.db')


class Entry(Model):
    title = TextField()
    date = DateField()
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE

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
