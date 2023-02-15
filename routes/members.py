from flask import Blueprint,request,jsonify
from controllers.members import addMember,history
members=Blueprint('members',__name__)
@members.route('/add',methods=['POST'])
def add():
    request_data=request.json
    response=addMember(request_data['name'],request_data['email'])
    return jsonify({"response":response}),200

@members.route('/history',methods=['POST'])
def view():
    request_data=request.json
    response=history(request_data['member_id'])
    return jsonify({"response":response}),200
