import pytest
import json
import requests
from app import Books

def test_add_books(client):
        # res= client.post('/book/add',json={
        #     "genre":"fiction"
        # })
        # assert res.status_code==400
    res2=client.post('/book/add',json={
        "genre":""
    })
    assert res2.status_code==400
    res3=client.post('/book/add',json={
        "genre":"1"
    })
    assert res3.status_code==400
    res4=client.post('/book/add',json={
        "genre":"dededededd"
    })
    assert res4.status_code==400

def test_edit_book(client):
    demoBook=Books(name="demobook",author="demoauthor",available=20,votes=20)
    demoBook_id=demoBook.id
    data1={
        "key":"name",
        "value":"demoBook2",
    }
    data2={
        "key":"author",
        "value":"demoauthor2"
    }
    res1=client.patch(f'/book/edit-book-data/{demoBook_id}',json=data1)
    assert res1.status_code==200
    res2=client.patch(f'/book/edit-book-data/{demoBook_id}',json=data2)
    assert res2.status_code==200
    demoBook.delete(demoBook_id)
    res3=client.patch(f'/book/edit-book-data/{demoBook_id}',json=data1)
    assert res3.status_code==404