from peewee import *

DATABASE = "boards.db"
# persist information
database = SqliteDatabase(DATABASE)

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database

# the user model specifies its fields (or columns) declaratively, like django
class Board(BaseModel):
    board = TextField()
    created_at = DateTimeField()

class Clue(BaseModel):
    board = ForeignKeyField(Board, backref="clues")
    word = TextField()
    hint = TextField()

if __name__ == "__main__":
    import os
    if "RESET" in os.environ:
        database.connect()
        database.create_tables([Board, Clue])
