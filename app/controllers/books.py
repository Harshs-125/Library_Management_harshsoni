from flask import Flask,jsonify
from sqlobject import *
from datetime import date
import requests
from ..constants import BOOK_API_URL
from ..models.books import Books
from ..models.members import Members
from ..models.transactions import Transactions

def addbooks(genre):
    try:
        url = f"{BOOK_API_URL}{genre}/2020"
        headers = {
	        "X-RapidAPI-Key": "b403235f84msh4b8a7702e4c9501p1b3b58jsn3ab0b7b79b85",
	        "X-RapidAPI-Host": "hapi-books.p.rapidapi.com"
        }
        response = requests.get(url,headers=headers)
        arr = response.json()
        for book in arr:
            b = Books(name=book["name"],author=book["author"],available=20,votes=book['votes'])
        return jsonify({"response":"following books have been added","books":arr}),200
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

def editBookData(id,data):
    try:
        book=Books.get(id)
    except SQLObjectNotFound:
        return jsonify({"response":"data not found"}),404
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400
    else:
        if(data['key']=="name"):
            book.name=data['value']
        elif(data['key']=="author"):
            book.author=data['value']
        elif(data['key']=="available"):
            book.available=data['value']
        return jsonify({"response":"book details successfully edited",
        "book":{
            "id":book.id,
            "name":book.name,
            "author":book.author,
            "available":book.available,
            "votes":book.votes
        }}),200

def borrowBook(book_id,data):
    try:
        memb_id=data['member_id']
        member=Members.get(memb_id)
        book=Books.get(book_id)
    except SQLObjectNotFound:
        return jsonify({"response":"member or book data not found"}),404
    except Exception as err:
        return jsonify({"response":"something is wrong"}),400
    else:
        if(member.debt>=500):
                return jsonify({"response":"cannot issue",
                "message":"clear your debt"}),400
        transaction=Transactions.selectBy(member_id=memb_id,book_id=book_id)
        if(list(transaction)!=[]):
            repeat_transaction=Transactions.selectBy(member_id=memb_id,book_id=book_id,status="issued")
            if(list(repeat_transaction)!=[]):
                return jsonify({"response":"cannot issue",
                "message":"cannot reissued the same book"}),400
            transaction=Transactions(book_id=book_id,member_id=memb_id)
            member.hasbooks=member.hasbooks+1
            member.totalbookissued=member.totalbookissued+1
            book.available=book.available-1
            book.votes=book.votes+1
            return jsonify({"response":"Book successfully issued",
            "transaction-id":transaction.id,
            "member-id":member.id,
            "book-id":book.id}),200
        else:
                transaction=Transactions(book_id=book_id,member_id=memb_id)
                member.hasbooks=member.hasbooks+1
                book.available=book.available-1
                return jsonify({"response":"Book successfully issued",
                "transaction-id":transaction.id,
                "member-id":member.id,
                "book-id":book.id}),200
        
def returnBookData(transaction_id,amount_paid):
    try:
        transaction=Transactions.get(transaction_id)
        member=Members.get(transaction.member_id)
        book=Books.get(transaction.book_id)
    except SQLObjectNotFound:
        return jsonify({"response":"data not found"}),404
    except Exception as err:
        return jsonify({"response":"something is wrong"}),400
    else:
        if(transaction.status=="returned"):
            return jsonify({"response":"book is already returned",
            }),200
        issued_date=transaction.issue_date
        current_date=date.today()
        delta = current_date-issued_date
        days=delta.days
        amount_to_paid=transaction.amount_to_paid
        if(days>15):
            fine=((current_date-issued_date)-15)*10
            amount_to_paid=amount_to_paid+fine
        transaction.return_date=current_date
        transaction.amount_to_paid=amount_to_paid
        transaction.amount_paid=amount_paid
        transaction.status="returned"
        book.available=book.available+1 
        if(amount_to_paid-amount_paid>0):
            member.debt=member.debt + (amount_to_paid-amount_paid)
        return jsonify({"response":"Success",
        "transaction_id":transaction.id,
        "book_id":transaction.book_id,
        "member_id":transaction.member_id,
        "amount_to_paid":transaction.amount_to_paid,
        "amount_paid":transaction.amount_paid,
        }),200

def getPopular(number):
    try:
        books=Books.select()
        books=list(books)
        books.sort(key=lambda x:x.votes,reverse=True)
        popular=[]
        for i in range (0,number):
            dict={}
            dict['id']=books[i].id
            dict['name']=books[i].name
            dict['author']=books[i].author
            dict['votes']=books[i].votes
            popular.append(dict)
        return jsonify({"response":f"the top {number} popular books","books":popular}),200
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400
    
def getBookByName(name):
    try:
        book=Books.selectBy(name=name)
        if(list(book)!=[]):
            return jsonify({"response":"Book with this name",
            "id":book[0].id,
            "name":book[0].name,
            "author":book[0].author,
            "votes":book[0].votes,
            }),200
        return jsonify({"message":"no book with this name"}),404
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

def getBookByAuthor(author):
    try:
        book=Books.selectBy(author=author)
        if(list(book)!=[]):
            arr=[]
            for b in book:
                dict={}
                dict['id']=b.id,
                dict['name']=b.name,
                dict['author']=b.author,
                dict['votes']=b.votes
                arr.append(dict)
            return jsonify({"response":"Book with this name",
            "books":arr 
            }),200
        return jsonify({"message":"no book with this name"}),404
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400
