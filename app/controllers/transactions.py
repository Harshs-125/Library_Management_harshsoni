from flask import Flask,jsonify
from datetime import date
from sqlobject import *
from ..models.transactions import Transactions
def viewrecord(transaction_id):
    try:
        transaction=Transactions.get(transaction_id)
    except SQLObjectNotFound:
        return jsonify({"response":"data not found"}),404
    else:
            issued_date=transaction.issue_date
            current_date=date.today()
            delta = current_date-issued_date
            days=delta.days
            amount_to_pay=100
            if(days>15):
                fine=((current_date-issued_date)-15)*10
                amount_to_pay=amount_to_pay+fine
            return jsonify({
            "response":"the record of this id",
            "transaction-id":transaction.id,
            "member_id":transaction.member_id,
            "book-id":transaction.book_id,
            "amount-to-pay":amount_to_pay,
            "amount_paid":transaction.amount_paid}),200