from flask import Blueprint,request,jsonify
from controllers.members import addMember,history,payDebt
members=Blueprint('members',__name__)
@members.route('/add',methods=['POST'])
def add():
    request_data=request.json
    response=addMember(request_data['name'],request_data['email'])
    return response

@members.route('/history',methods=['POST'])
def view():
    request_data=request.json
    response=history(request_data['member_id'])
    return response

@members.route('/paydebt/<int:id>',methods=['POST'])
def paydebt(id):
    request_data=request.json
    response=payDebt(id,request_data['amount'])
    return response
