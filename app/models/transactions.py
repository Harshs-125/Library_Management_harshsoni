from sqlobject import *

from datetime import datetime

class Transactions(SQLObject):
    class sqlmeta:
        table = "transactions"
    book_id=IntCol(notNone=False)
    member_id=IntCol(notNone=False)
    issue_date=DateCol(notNone=False,default=datetime.now().date())
    return_date=DateCol(default=None)
    status=StringCol(default="issued")
    amount_to_paid=IntCol(notNone=False,default=100)
    amount_paid=IntCol(notNone=False,default=0) 
    
    def get_dict(self):
        return {'id':self.id,'book_id':self.book_id,'member_id':self.member_id,'issue_date':self.issue_date,'return_date':self.return_date,'status':self.status,'amount_to_paid':self.amount_to_paid,'amount_paid':self.amount_paid}



