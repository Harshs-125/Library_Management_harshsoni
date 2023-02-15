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
    amount_to_paid=IntCol(notNone=False,default=0)
    amount_paid=IntCol(notNone=False,default=0) 
    


