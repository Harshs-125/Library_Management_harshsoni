from flask import Flask,jsonify
import requests
from models.members import Members
from models.transactions import Transactions

def addMember(name,e):
    try:
        mem=Members.select(Members.q.email==e)
        if(mem.count()>0):
            return jsonify({"response":"member with this email id already exits"}),409
        member=Members(name=name,email=e)
        return jsonify({"response":"member created successfully"}),200
    except Exception:
        return jsonify({"response":"Internal Server Error"}),500

def history(id):
    try:
        member=Members.selectBy(id=id)
        arr=[]
        if(list(member)!=[]):
            transactions=Transactions.selectBy(member_id=id)
            if(list(transactions)==[]):
                return jsonify({"response":"no transactions of this member"}),404
            for transaction in transactions:
                arr.append(Transactions.get_dict(transaction))
            return jsonify({"response":"success fully fetched data",
            "name":member[0].name,
            "debt":member[0].debt,
            "totalbooks":member[0].hasbooks,
            "transactions":arr
            }),200
        return jsonify({"response":"member not found with this id"}),404
    except Exception:
        return jsonify({"response":"Internal Server Error"}),500

def payDebt(id,amount):
    try:
        member=Members.selectBy(id=id)
        if(list(member)!=[]):
            member[0].debt=member[0].debt-amount
            return jsonify({"response":"amount registered"}),200
        return jsonify({"response":"member not found with this id"}),404
    except Exception:
        return jsonify({"response":"Internal Server Error"}),500
