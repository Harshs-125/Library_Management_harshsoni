from flask import Flask,jsonify
from datetime import date,datetime
import requests
from sqlobject import SQLObjectNotFound
from models.transactions import Transactions
def viewrecord(transaction_id):
    try:
        transaction=Transactions.select(Transactions.q.id == transaction_id)
        if(list(transaction) != []):
            issued_date=transaction[0].issue_date
            current_date=date.today()
            delta = current_date-issued_date
            days=delta.days
            amount_to_pay=100
            if(days>15):
                fine=((current_date-issued_date)-15)*10
                amount_to_pay=amount_to_pay+fine
            return jsonify({
            "response":"the record of this id",
            "transaction-id":transaction[0].id,
            "member_id":transaction[0].member_id,
            "book-id":transaction[0].book_id,
            "amount-to-pay":amount_to_pay}),200
        return jsonify({"response":"No record found"}),404
    except Exception:
        return jsonify({"response":"Internal Server Error"}),500
    
    


