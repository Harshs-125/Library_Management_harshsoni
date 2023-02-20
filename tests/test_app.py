import pytest
import requests
# from app.models.transactions import Transactions
# # def test_request_example(client):
# #     response = client.get("/")

# #     assert response.status_code == 200

def test_app1():
    res=requests.get('http://127.0.0.1:5000')
    assert res.status_code==200

def test_app2():
    res=requests.get('http://127.0.0.1:5000')
    assert res.status_code==200

def test_app3():
    res=requests.get('http://127.0.0.1:5000')
    assert res.status_code==200


# def record():
#     res=requests.get(' http://127.0.0.1:5000/transaction/viewrecord/1')
#     data=res.json()
#     assert  res.status_code==200
#     transaction=Transactions.selectBy(id=1)
#     assert res.transaction_id==transaction[0].id

def test_app(client):
    res=client.get('/')
    assert res.status_code==200

