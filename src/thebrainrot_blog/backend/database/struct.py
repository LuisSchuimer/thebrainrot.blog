"""
SQLite database structure for thebrainrot.blog written by Luis Schuimer
"""

from peewee import (
    SqliteDatabase,
    Model,
    TextField,
    DateTimeField,
    IntegerField
)
from datetime import datetime


db = SqliteDatabase("posts.db")

class BaseModel(Model):
    class Meta:
        database = db

class Posts(BaseModel):
    id = TextField(primary_key=True) # UUID 4 
    title = TextField()
    author = TextField()
    content = TextField() # Content as string
    render_file = TextField() # File where rendered content is saved
    date = DateTimeField(default=datetime.now) # Creation date

class Keywords(BaseModel):
    word = TextField(primary_key=True) # Keyword as str
    x = IntegerField() # X value from tokenizer
    y = IntegerField() # Y value from tokenizer

"Builds the database with created tables and rows"
def build() -> SqliteDatabase:
    db.connect()
    db.create_tables([Posts, Keywords]) # type: ignore
    return db