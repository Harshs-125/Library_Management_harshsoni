from flask import Flask
from datetime import datetime,date
import requests
from constants import BOOK_API_URL
from models.books import Books

def addbooks(genre):
    url = f"{BOOK_API_URL}{genre}/2020"
    headers = {
	    "X-RapidAPI-Key": "b403235f84msh4b8a7702e4c9501p1b3b58jsn3ab0b7b79b85",
	    "X-RapidAPI-Host": "hapi-books.p.rapidapi.com"
    }
    response = requests.get(url,headers=headers)
    arr = response.json()
    print('hi')
    for book in arr:
        print('hello')
        b = Books(name=book["name"],author=book["author"],available=20,votes=book['votes'])
        print(b)
        print('bye')
    print('bye')
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