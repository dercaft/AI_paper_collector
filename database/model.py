
import peewee
from peewee import *
db=peewee.SqliteDatabase('papers.sqlite3')
HEAD=[
    "title",
    "conference",
    "year",
    "abstract",
    "abstract_link",
    "pdf_link",
]
class Paper(peewee.Model):
    title=CharField(max_length=2048)
    conference=CharField()
    year=IntegerField()
    abstract=TextField()
    abstract_link=CharField(max_length=1024)
    pdf_link=CharField(max_length=1024)
    class Meta:
        database=db
    pass