from flask import Blueprint,request,jsonify
from controllers.members import addMember
members=Blueprint('members',__name__)
@members.route('/add',methods=['POST'])
def add():
    request_data=request.json
    response=addMember(request_data['name'],request_data['email'])
    return jsonify({"response":response}),200