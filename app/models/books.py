from sqlobject import *
 
class Books(SQLObject):
    class sqlmeta:
        table = "books"
    name=StringCol(notNone=False)
    author=StringCol(notNone=False)
    votes=IntCol(notNone=False)
    available=IntCol(notNone=False)

    def get_dict(self):
        return {'id':self.id,'name':self.name,'votes':self.votes,'available':self.available}