from flask import Flask
import requests
from models.members import Members

def addMember(name,e):
    mem=Members.select(Members.q.email==e)
    if(mem.count()>0):
        return "member already exits"
    member=Members(name=name,email=e)
    return "member added successfully"