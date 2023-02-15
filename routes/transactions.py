from flask import Blueprint,request,jsonify
from controllers.transactions import viewrecord

transaction=Blueprint('transaction',__name__)


@transaction.route('/viewrecord',methods=['POST'])
def view():
    request_data=request.json
    response=viewrecord(request_data)
    return jsonify({
        "response":response
    }),200