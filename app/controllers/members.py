from flask import Flask,jsonify
from sqlobject import *
from ..models.members import Members
from ..models.transactions import Transactions

def addMember(name,e):
    try:
        mem=Members.select(Members.q.email==e)
        if(mem.count()>0):
            return jsonify({"response":"member with this email id already exits"}),409
        member=Members(name=name,email=e)
        return jsonify({"response":"member created successfully","member-id":member.id,"member-name":member.name,"member-email":member.email}),200
    except Exception as err:
       return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

def history(id):
    try:
        member=Members.get(id=id)
    except SQLObjectNotFound:
        return jsonify({"response":"data not found"}),404
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400
    else:
        transactions=Transactions.selectBy(member_id=id)
        arr=[]
        for transaction in transactions:
            arr.append(Transactions.get_dict(transaction))
        return jsonify({"response":"success fully fetched data",
        "name":member.name,
        "debt":member.debt,
        "totalbooks":member.hasbooks,
        "transactions":arr
        }),200

def payDebt(id):
    try:
        member=Members.get(id)
    except SQLObjectNotFound:
        return jsonify({"response":"data not found"}),404
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400
    else:    
        member.debt=0
        return jsonify({"response":"debt cleared"}),200

def highestPayingCustomer(number):
    try:
        members=Members.select()
        members=list(members)
        members.sort(key=lambda x:x.totalbookissued,reverse=True)
        print(members)
        customers=[]
        num=[number,len(members)]
        n=min(num)
        for i in range (0,n):
            dict={}
            dict['id']=members[i].id
            dict['name']=members[i].name
            dict['author']=members[i].email
            dict['totalbookissued']=members[i].totalbookissued
            customers.append(dict)
        return jsonify({"response":f"the top {n} paying customers","customers":customers}),200
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

def deleteMember(member_id):
    try:
        member=Members.get(member_id)
    except SQLObjectNotFound:
        return jsonify({"response":"object not found with this data"}),404
    else:
        if(member.debt!=0 or member.hasbooks!=0):
            return jsonify({"response":"failed","message":"cannot delete the member since record is not clear"}),400
        member.delete(member_id)
        return jsonify({"response":"successfully deleted the member"}),200
         
def updateMember(member_id,data):
    try:
        member=Members.get(member_id)
    except SQLObjectNotFound:
        return jsonify({"response":"object not found with this data"}),404
    else:
        if(data['key']=="name"):
            member.name=data['value']
        if(data['key']=="email"):
            member.email==data['value']
        return jsonify({"response":"member details successfully updated",
                        "member":{
                        "id":member.id,
                        "name":member.name,
                        "email":member.email,
                        }}),200