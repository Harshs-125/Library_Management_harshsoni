from sqlobject import *
 
class Books(SQLObject):
    class sqlmeta:
        table = "books"
    name=StringCol(notNone=False)
    author=StringCol(notNone=False)
    votes=IntCol(notNone=False)
    available=IntCol(notNone=False)


