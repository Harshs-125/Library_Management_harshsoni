from flask import Blueprint,request,jsonify
from controllers.members import addMember,history,payDebt
members=Blueprint('members',__name__)
@members.route('/add',methods=['POST'])
def add():
    request_data=request.json
    response=addMember(request_data['name'],request_data['email'])
    return response

@members.route('/history/<int:member_id>',methods=['GET'])
def view(member_id):
    response=history(member_id)
    return response

@members.route('/paydebt/<int:member_id>',methods=['POST'])
def paydebt(member_id):
    request_data=request.json
    response=payDebt(member_id,request_data['amount'])
    return response
