from flask import Blueprint,request,jsonify
from controllers.books import addbooks,editBookData,borrowBook,returnBookData,getPopular
books=Blueprint('books',__name__)
@books.route('/add',methods=['POST'])
def add():
    request_data=request.json
    response=addbooks(request_data['genre'])
    print("response")
    return jsonify({"response":response}),200

@books.route('/edit-book-data',methods=['PATCH'])
def edit():
    request_data=request.json
    response=editBookData(request_data)
    return jsonify({
        "response":response
    }),200

@books.route('/borrow',methods=['POST'])
def borrow():
    request_data=request.json
    response=borrowBook(request_data)
    return jsonify({
     "response":response
    }),200
@books.route('/return',methods=['POST'])
def returnBook():
    request_data=request.json
    response=returnBookData(request_data)
    return jsonify({
        "response":response
    }),200

@books.route('/popular/<int:number>',methods=['GET'])
def popularBook(number):
    response=getPopular(number)
    return jsonify({
        "response":response
    }),200