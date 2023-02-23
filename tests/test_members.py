import pytest
import json
from app import Members
def test_create_member(client):
    data1={
        "name":"demo",
        "email":"demo@1234"
    }
    res1=client.post('/member/add',json=data1)
    demomember_id=res1.json['member-id']
    res2=client.post('/member/add',json=data1)
    member=Members.get(demomember_id)
    member.delete(demomember_id)
    assert res1.status_code==200
    assert res2.status_code==409

def test_member_transaction_history(client,create_member):
    demomember=create_member
    member_id=demomember.id
    res1=client.get(f'/member/history/{member_id}')
    assert res1.status_code==200
    assert res1.json['name']==demomember.name
    assert res1.json['transactions']!=None
    demomember.delete(member_id)
    res2=client.get(f'/member/history/{member_id}')
    assert res2.status_code==404


def test_paydebt(client,create_member):
    demomember=create_member
    demomember.debt=100
    member_id=demomember.id
    res1=client.post(f'/member/paydebt/{member_id}',json={"amount":50})
    assert res1.status_code==200
    demomember.delete(member_id)

def test_highestpaying_customer(client):
   res1=client.get('/member/highestpayingcustomer/2')
   assert res1.status_code==200

def test_delete_member(client,create_member):
    demomember=create_member
    member_id=demomember.id
    demomember.debt=100
    res2=client.delete(f'/member/delete/{member_id}')
    assert res2.status_code==400
    demomember.debt=0
    demomember.hasbooks=1
    res3=client.delete(f'/member/delete/{member_id}')
    assert res3.status_code==400
    demomember.hasbooks=0
    res1=client.delete(f'/member/delete/{member_id}')
    assert res1.status_code==200
    res4=client.delete(f'/member/delete/{member_id}')
    assert res4.status_code==404