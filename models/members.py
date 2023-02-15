
from sqlobject import *

class Members(SQLObject):
    class sqlmeta:
        table = "members"
    name=StringCol(notNone=False)
    email=StringCol(notNone=False,unique=True)
    hasbooks=IntCol(default=0)
    debt=IntCol(default=0)

    def get_dict(self):
        return {'id':self.id,'name':self.name,'email':self.email,'hasbooks':self.hasbooks,'debt':self.debt}
