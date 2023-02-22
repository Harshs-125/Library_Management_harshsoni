import pytest
import json
from app import Members
def test_create_member(client):
    data1={
        "name":"demo",
        "email":"demo@123"
    }
    res1=client.post('/member/add',json=data1)
    demomember_id=res1.json['member-id']
    res2=client.post('/member/add',json=data1)
    member=Members.get(demomember_id)
    member.delete(demomember_id)
    assert res1.status_code==200
    assert res2.status_code==409


def test_delete_member(client):
    demomember=Members(name="demo",email="demo@123")
    member_id=demomember.id
    res1=client.delete(f'/member/delete/{member_id}')
    assert res1.status_code==200
    res2=client.delete('/member/delete')
    assert res2.status_code==404

def test_member_transaction_history(client):
    demomember=Members(name="demo",email="demo@123")
    member_id=demomember.id
    res1=client.get(f'/member/history/{member_id}')
    assert res1.status_code==200
    assert res1.json['name']=="demo"
    assert res1.json['transactions']!=None
    demomember.delete(member_id)
    res2=client.get(f'/member/history/{member_id}')
    assert res2.status_code==404

@pytest.mark.skip
def test_paydebt(client):
    demomember=Members(name="demo",email="demo@123")
    demomember.debt=100
    member_id=demomember.id
    res1=client.get(f'/member/paydebt/{member_id}',post={"amount":50})
    assert res1.status_code==200
    demomember.delete(member_id)

def test_highestpaying_customer(client):
   res1=client.get('/member/highestpayingcustomer/2')
   assert res1.status_code==200

def test_delete_member(client):
    demomember=Members(name="demo",email="demo@123")
    member_id=demomember.id
    res1=client.delete(f'/member/delete/{member_id}')
    assert res1.status_code==200
    res2=client.delete(f'/member/delete/{member_id}')
    assert res2.status_code==404