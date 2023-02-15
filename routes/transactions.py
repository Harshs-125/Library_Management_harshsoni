from flask import Blueprint,request,jsonify
from controllers.transactions import viewrecord

transaction=Blueprint('transaction',__name__)


@transaction.route('/viewrecord/<int:transaction_id>',methods=['GET'])
def view(transaction_id):
    response=viewrecord(transaction_id)
    return response