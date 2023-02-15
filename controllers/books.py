from flask import Flask
from datetime import datetime,date
import requests
from constants import BOOK_API_URL
from models.books import Books
from models.members import Members
from models.transactions import Transactions

def addbooks(genre):
    url = f"{BOOK_API_URL}{genre}/2020"
    headers = {
	    "X-RapidAPI-Key": "b403235f84msh4b8a7702e4c9501p1b3b58jsn3ab0b7b79b85",
	    "X-RapidAPI-Host": "hapi-books.p.rapidapi.com"
    }
    response = requests.get(url,headers=headers)
    arr = response.json()
    for book in arr:
        b = Books(name=book["name"],author=book["author"],available=20,votes=book['votes'])
    return arr

def editBookData(data):
    book_id=data["book_id"]
    book=Books.get(id=book_id)
    if(book): 
        if(data['key']=="name"):
          book.name=data['value']
        elif(data['key']=="author"):
            book.author=data['value']
        elif(data['key']=="available"):
            book.available=data['value']
        return "book details is edited"
    else:
        return "no book with the given id "
def borrowBook(data):
    memb_id=data['member_id']
    b_id=data['book_id']
    member=Members.selectBy(id=memb_id)[0]
    book=Books.selectBy(id=b_id)[0]
    transaction=Transactions.selectBy(member_id=memb_id,book_id=b_id)

    if(list(transaction)!=[]):
        repeat_transaction=Transactions.selectBy(member_id=memb_id,book_id=b_id,status="issued")
        if(list(repeat_transaction)!=[]):
            return "this book is already issued to this member cannot reissue the same book"
        if(member.debt>=500):
            return "cannot issue the book since members dept is exceeding the limit"
        transaction=Transactions(book_id=b_id,member_id=memb_id)
        member.hasbooks=member.hasbooks+1
        book.available=book.available-1
        return "book is issued to the member"
    else:
            transaction=Transactions(book_id=b_id,member_id=memb_id)
            member.hasbooks=member.hasbooks+1
            book.available=book.available-1
            return "book is issued to the member"

def returnBookData(data):
    transation_id=data['id']
    transaction=Transactions.selectBy(id=transation_id)
    if(list(transaction)!=[]):
        member=Members.selectBy(id=transaction[0].member_id)[0]
        book=Books.selectBy(id=transaction[0].book_id)[0]
        amount_paid=data['amount_paid']
        issued_date=transaction[0].issue_date
        current_date=date.today()
        delta = current_date-issued_date
        days=delta.days
        amount_to_paid=transaction[0].amount_to_paid
        if(days>15):
            fine=((current_date-issued_date)-15)*10
            amount_to_paid=amount_to_paid+fine
        transaction[0].return_date=current_date
        transaction[0].amount_to_paid=amount_to_paid
        transaction[0].amount_paid=amount_paid
        transaction[0].status="returned"
        member.hasbooks=member.hasbooks-1
        book.available=book.available+1 
        if(amount_to_paid-amount_paid>0):
            member.debt=member.debt + (amount_to_paid-amount_paid)
        return "successfully record the returned data "
    return "no such transaction found"
    