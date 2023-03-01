from flask import Blueprint,request
from ..controllers.books import addbooks,editBookData,borrowBook,returnBookData,getPopular,getBookByName,getBookByAuthor,getBookByID
books=Blueprint('books',__name__)
@books.route('/add',methods=['POST'])
def add():
    request_data=request.json
    response=addbooks(request_data['genre'])
    return response

@books.route('/edit-book-data/<int:id>',methods=['PATCH'])
def edit(id):
    request_data=request.json
    response=editBookData(id,request_data)
    return response

@books.route('/borrow/<int:id>',methods=['POST'])
def borrow(id):
    request_data=request.json
    response=borrowBook(id,request_data)
    return response
@books.route('/return/<int:transaction_id>',methods=['POST'])
def returnBook(transaction_id):
    amount_paid=request.json['amount_paid']
    response=returnBookData(transaction_id,amount_paid)
    return response

@books.route('/popular/<int:number>',methods=['GET'])
def popularBook(number):
    response=getPopular(number)
    return response
@books.route('/searchbyname/<string:name>',methods=['GET'])
def getbyname(name):
    response=getBookByName(name)
    return response

@books.route('/searchbyauthor/<string:author>',methods=['GET'])
def getbyauthor(author):
    response=getBookByAuthor(author)
    return response

@books.route('/searchbyid/<int:id>',methods=['GET'])
def getbyid(id):
    response=getBookByID(id)
    return response
