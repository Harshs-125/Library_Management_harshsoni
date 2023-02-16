from flask import Flask,jsonify
from models.members import Members
from models.transactions import Transactions

def addMember(name,e):
    try:
        mem=Members.select(Members.q.email==e)
        if(mem.count()>0):
            return jsonify({"response":"member with this email id already exits"}),409
        member=Members(name=name,email=e)
        return jsonify({"response":"member created successfully"}),200
    except Exception as err:
       return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

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
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

def payDebt(id,amount):
    try:
        member=Members.selectBy(id=id)
        if(list(member)!=[]):
            member[0].debt=member[0].debt-amount
            return jsonify({"response":"amount registered"}),200
        return jsonify({"response":"member not found with this id"}),404
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

def highestPayingCustomer(number):
    try:
        members=Members.select()
        members=list(members)
        members.sort(key=lambda x:x.totalbookissued,reverse=True)
        print(members)
        customers=[]
        for i in range (0,number):
            dict={}
            dict['id']=members[i].id
            dict['name']=members[i].name
            dict['author']=members[i].email
            dict['votes']=members[i].totalbookissued
            customers.append(dict)
        return jsonify({"response":f"the top {number} paying customers","customers":customers}),200
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400
