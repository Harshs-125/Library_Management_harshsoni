from flask import Flask
import requests
from models.members import Members
from models.transactions import Transactions

def addMember(name,e):
    mem=Members.select(Members.q.email==e)
    if(mem.count()>0):
        return "member already exits"
    member=Members(name=name,email=e)
    return "member added successfully"

def history(id):
    member=Members.selectBy(id=id)
    arr=[]
    if(list(member)!=[]):
        transactions=Transactions.selectBy(member_id=id)
        if(list(transactions)==[]):
            return "no transactions of this member"
        for transaction in transactions:
            arr.append(Transactions.get_dict(transaction))
        return {'transactions':arr,'debt':member[0].debt,'total_books':member[0].hasbooks}
    return "no member with this id "