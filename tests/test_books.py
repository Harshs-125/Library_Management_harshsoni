import pytest
import json
import requests
from app import Books,Members,Transactions

@pytest.mark.skip
def test_add_books(client):
    res= client.post('/book/add',json={
        "genre":"romance"
    })
    assert res.status_code==400
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
    assert res1.json['book']!={}
    res2=client.patch(f'/book/edit-book-data/{demoBook_id}',json=data2)
    assert res2.status_code==200
    assert res2.json['book']!={}
    demoBook.delete(demoBook_id)
    res3=client.patch(f'/book/edit-book-data/{demoBook_id}',json=data1)
    assert res3.status_code==404
    assert res3.json['response']=="data not found"
# @pytest.mark.skip
def test_borrow_book_and_return(client):
    demoBook=Books(name="demobook",author="demoauthor",available=20,votes=20)
    demomember=Members(name="demomember",email="demoemail@123")
    demobook_id=demoBook.id
    demomember_id=demomember.id
    res1=client.post(f'/book/borrow/{demobook_id}',json={"member_id":demomember_id})
    transaction_id=res1.json['transaction-id']
    transaction=Transactions.get(transaction_id)
    assert res1.status_code==200
    assert res1.json['member-id']==demomember_id
    assert res1.json['book-id']==demobook_id
    assert res1.json['transaction-id']!=None
    res2=client.post(f'/book/borrow/{demobook_id}',json={"member_id":demomember_id})
    assert res2.status_code==400
    assert res2.json['response']=="cannot issue"
    assert res2.json['message']=="cannot reissued the same book"
    amountpaid=100
    res5=client.post(f'/book/return/{transaction_id}',json={"amount_paid":amountpaid})
    assert res5.status_code==200
    assert res5.json['response']=="Success"
    assert res5.json['book_id']==demobook_id
    assert res5.json['member_id']==demomember_id
    assert res5.json['amount_to_paid']==transaction.amount_to_paid
    assert res5.json['amount_paid']==transaction.amount_paid
    Transactions.delete(transaction_id)
    Members.delete(demomember_id)
    Books.delete(demobook_id)
    demoBook=Books(name="demobook",author="demoauthor",available=20,votes=20)
    demomember=Members(name="demomember",email="demoemail@123")
    demobook_id=demoBook.id
    demomember_id=demomember.id
    demomember.debt=600
    res3=client.post(f'/book/borrow/{demobook_id}',json={"member_id":demomember_id})
    assert res3.status_code==400
    assert res3.json['response']=="cannot issue"
    assert res3.json['message']=="clear your debt"
    
    res4=client.post(f'/book/borrow/{0}',json={"member_id":0})
    assert res4.status_code==404
    assert res4.json['response']=="member or book data not found"
    
    
    

