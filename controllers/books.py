from flask import Flask,jsonify
from datetime import date
import requests
from constants import BOOK_API_URL
from models.books import Books
from models.members import Members
from models.transactions import Transactions

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
        book=Books.selectBy(id=id)
        if(list(book)!=[]): 
            if(data['key']=="name"):
                book.name=data['value']
            elif(data['key']=="author"):
                book.author=data['value']
            elif(data['key']=="available"):
                book.available=data['value']
            return jsonify({"response":"book details successfully edited"}),200
        else:
            return jsonify({"response":"No book found with this id"}),404
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

def borrowBook(book_id,data):
    try:
        memb_id=data['member_id']
        member=Members.selectBy(id=memb_id)[0]
        book=Books.selectBy(id=book_id)[0]  
        transaction=Transactions.selectBy(member_id=memb_id,book_id=book_id)
        if(list(transaction)!=[]):
            repeat_transaction=Transactions.selectBy(member_id=memb_id,book_id=book_id,status="issued")
            if(list(repeat_transaction)!=[]):
                return jsonify({"response":"this book is already issued to this member cannot reissue the same book"}),200
            if(member.debt>=500):
                return jsonify({"response":"cannot issue the book since members dept is exceeding the limit first clear the debt"}),200
            transaction=Transactions(book_id=book_id,member_id=memb_id)
            member.hasbooks=member.hasbooks+1
            member.totalbooksissued=member.totalbooksissued+1
            book.available=book.available-1
            book.votes=book.votes+1
            return jsonify({"response":"Book successfully issued"}),200
        else:
                transaction=Transactions(book_id=book_id,member_id=memb_id)
                member.hasbooks=member.hasbooks+1
                book.available=book.available-1
                return jsonify({"response":"Books successfully issued"}),200
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400
        
def returnBookData(transaction_id,amount_paid):
    try:
        transaction=Transactions.selectBy(id=transaction_id)
        if(list(transaction)!=[]):
            member=Members.selectBy(id=transaction[0].member_id)[0]
            book=Books.selectBy(id=transaction[0].book_id)[0]
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
            return jsonify({"response":"successfully recorded the returned data"}),200
        return jsonify({"response":"no such transaction found"})
    except Exception as err:
        return jsonify({"response":"Something went wrong",
        "error":str(err)}),400

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
