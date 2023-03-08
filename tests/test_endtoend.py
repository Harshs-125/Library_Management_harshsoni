import pytest
from app import Books,Members,Transactions

def test_endtoend_positive(client):
    book=Books(name="demobook",author="demoauthor",available=1,votes=0)
    book_id=book.id
    data1={
        "name":"DemoUser",
        "email":"demoemail@123.com"
    }
    res1=client.post('/member/add',json=data1)
    member_id=res1.json['member-id']
    assert res1.status_code==200
    assert res1.json['response']=="member created successfully"
    assert res1.json['member-id']!=None

    res2=client.post(f'/book/borrow/{book_id}',json={"member_id":member_id})
    transaction_id=res2.json['transaction-id']
    assert res2.status_code==200
    assert res2.json['response']=="Book successfully issued"
    assert res2.json['transaction-id']!=None
    book=Books.get(book_id)
    assert book.available==0
    assert book.votes==1

    res3=client.patch(f'/book/edit-book-data/{book_id}',json={"key":"available","value":1})
    assert res3.status_code==200
    assert book.available==1   
    assert res3.json['response']=="book details successfully edited" 
    assert res3.json['book']!={}

    res4=client.get(f'transaction/viewrecord/{transaction_id}')
    amount_to_pay=res4.json['amount-to-pay']
    assert res4.status_code==200
    amount_to_pay=res4.json['amount-to-pay']
    assert res4.status_code==200

    amount_paid=50
    res5=client.post(f'/book/return/{transaction_id}',json={"amount_paid":amount_paid})
    assert res5.status_code==200
    assert res5.json['response']=="Success"
    assert res5.json['book_id']==book_id
    assert res5.json['member_id']==member_id
    assert res5.json['amount_to_paid']==amount_to_pay
    assert res5.json['amount_paid']==amount_paid
    member=Members.get(member_id)
    assert amount_to_pay-amount_paid==member.debt

    res6=client.get(f'/member/history/{member_id}')
    assert res6.status_code==200
    assert res6.json['name']==member.name
    assert res6.json['transactions']!=None

    res7=client.post(f'/member/paydebt/{member_id}')
    assert res7.status_code==200
    assert member.debt==0

    res8=client.get('/member/highestpayingcustomer/2')
    assert res8.status_code==200

    res9=client.post(f'/book/searchbyname',json={"name":"demobook"})
    assert res9.status_code==200
    assert res9.json['name']==book.name

    res10=client.post(f'/book/searchbyauthor',json={"author":"demoauthor"})
    assert res10.status_code==200
    assert res10.json['books']!=[]

    res11=client.get('/book/popular/2')
    assert res11.status_code==200
    
    res12=client.delete(f'/member/delete/{member_id}')
    assert res12.status_code==200

    Books.delete(book_id)
    Transactions.delete(transaction_id)

def test_endtoend_negative(client):
    
    res2=client.post(f'/book/borrow/{0}',json={"member_id":0})
    assert res2.status_code==404
    assert res2.json['response']=="member or book data not found"

    res3=client.patch(f'/book/edit-book-data/{0}',json={"key":"available","value":1})
    assert res3.status_code==404
    assert res3.json['response']=="data not found"

    res4=client.get(f'transaction/viewrecord/{0}')
    assert res4.status_code==404

    res5=client.post(f'/book/return/{0}',json={"amount_paid":100})
    assert res5.status_code==404
    assert res5.json['response']=="data not found"

    res6=client.get(f'/member/history/{0}')
    assert res6.status_code==404

    res7=client.post(f'/member/paydebt/{0}')
    assert res7.status_code==404

    res9=client.post(f'/book/searchbyname',json={"name":"bsss"})
    assert res9.status_code==404
    assert res9.json['response']=="no book with this name"

    res10=client.post(f'/book/searchbyauthor',json={"author":"demoauthor"})
    assert res10.status_code==404
    
    member=Members(name="demo",email="demo@123")
    member.debt=100
    member.hasbooks=1
    res11=client.delete(f'/member/delete/{member.id}')
    assert res11.status_code==400
    assert res11.json['message']=="cannot delete the member since record is not clear"
    member.delete(member.id)