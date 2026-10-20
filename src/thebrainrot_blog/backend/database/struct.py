"""
SQLite database structure for thebrainrot.blog written by Luis Schuimer
"""

from peewee import (
    SqliteDatabase,
    Model,
    TextField,
    DateTimeField
)
from datetime import datetime


db = SqliteDatabase("posts.db")

class BaseModel(Model):
    class Meta:
        database = db

class Posts(BaseModel):
    id = TextField(primary_key=True)
    title = TextField()
    author = TextField()
    content = TextField()
    rendered_content = TextField()
    date = DateTimeField(default=datetime.now)

"Builds the database with created tables and rows"
def build() -> SqliteDatabase:
    db.connect()
    db.create_tables([Posts]) # type: ignore
    return db